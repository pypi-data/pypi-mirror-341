from fabric import Connection
import os
from .logger import update_version_log

def deploy_project(conf, dry_run=False):
    def run_cmd(conn, cmd, desc=None):
        if desc:
            print(f"\\n🔧 {desc}")
        print(f"→ {cmd}")
        if not dry_run:
            conn.run(cmd)

    print("🚀 Starting Django deployment...")

    if not os.path.exists(conf['env_file']):
        raise FileNotFoundError(f"⚠️ .env file not found at {conf['env_file']}")

    with Connection(conf['host']) as conn:
        with conn.cd(conf['remote_dir']):
            run_cmd(conn, f"git pull origin {conf['branch']}", "Pulling code")
            run_cmd(conn, f"{conf['venv_activate']} && pip install -r requirements.txt", "Installing requirements")

            print("📁 Uploading .env...")
            if not dry_run:
                conn.put(conf['env_file'], remote=conf['remote_dir'] + "/.env")

            run_cmd(conn, f"{conf['venv_activate']} && {conf['django_manage_path']} makemigrations", "Making migrations")
            run_cmd(conn, f"{conf['venv_activate']} && {conf['django_manage_path']} migrate", "Migrating database")
            run_cmd(conn, f"{conf['venv_activate']} && {conf['django_manage_path']} collectstatic --noinput", "Collecting static")

            if conf.get("restart_command"):
                run_cmd(conn, conf['restart_command'], "Restarting service")

    if not dry_run:
        update_version_log()

    print("\\n✅ Deployment complete.")
