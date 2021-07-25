import os
import tempfile
import getpass
from textwrap import dedent

def setup_shiny():
    '''Manage a Shiny instance.'''

    user_dir = "/net/mraid14/export/tgdata/db/tgdb/tanaywiz/users/{user}".format(user=getpass.getuser())
    os.makedirs(user_dir)
    os.makedirs(os.path.join(user_dir, "apps"))
    os.makedirs(os.path.join(user_dir, "logs"))
    os.makedirs(os.path.join(user_dir, "bookmarks"))

    name = 'shiny'
    def _get_shiny_cmd(port):
        conf = dedent("""
            run_as {user};
            preserve_logs on;
            server {{
                listen {port};
                location / {{
                    site_dir {user_dir}/apps;
                    log_dir {user_dir}/logs;
                    bookmark_state_dir {user_dir}/bookmarks;
                    directory_index on;

                    # Increased Idle timeout
                    app_idle_timeout 0;

                    log_file_mode 0774;
                }}
            }}
        """).format(
            user_dir=user_dir,
            port=str(port)            
        )

        f = tempfile.NamedTemporaryFile(mode='w', delete=False)
        f.write(conf)
        f.close()
        return ['shiny-server', f.name]

    return {
        'command': _get_shiny_cmd,
        'launcher_entry': {
            'title': 'Shiny',
            'icon_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons', 'shiny.svg')
        }
    }
