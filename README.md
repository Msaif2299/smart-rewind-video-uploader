# Smart Rewind Video Uploader

In order to use the video uploader, an AWS account must be configured. Go to https://aws.amazon.com to create an account.
Once the account is created, follow the steps:

- Install AWS CLI from https://aws.amazon.com/cli/
- Create a file named "credentials" in the location "~/.aws/"
- Add the following information, replace YOUR_ACCESS_KEY and YOUR_SECRET_KEY with values from your account
  ```
  [default]
  aws_access_key_id = YOUR_ACCESS_KEY
  aws_secret_access_key = YOUR_SECRET_KEY
  ```
- Create a file named "config" in the location "~/.aws/" and put the region of your account
  ```
  [default]
  region=us-east-1
  ```

Now if you run the .exe file, it should work.
If you wish to run the overall project, run the following command:
`py ./smartrewind/main.py`

To generate the pytest coverage report in the console first navigate to the root of this project, then run the commands:

- `pytest --cov ./smartrewind/backend`
- `pytest --cov ./smartrewind/logger`

To generate the pytest coverage report in the HTML format:

- `pytest --cov --cov-report=html:./htmlcov_backend ./smartrewind/backend`
- `pytest --cov --cov-report=html:./htmlcov_logger ./smartrewind/logger`
