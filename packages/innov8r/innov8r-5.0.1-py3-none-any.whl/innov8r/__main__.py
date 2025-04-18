from innov8r import launch, report_time
from innov8r.flask_app import startFlaskApp
from innov8r.login_validator import openLoginScreen, LoginApp


startFlaskApp()
report_time("Before launch")
launch()
