import subprocess

if __name__ == '__main__':
    subprocess.check_output(('psql --host=catappdatabase.cjlis1fysyzx.us-west-1.rds.amazonaws.com --port=5432 --username=catappuser --dbname=catappdatabase --password').split())
