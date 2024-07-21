# build_files.sh
pip3 install -r requirements.txt
python3 manage.py collectstatic
mkdir -p staticfiles_build/media
cp -r media/* staticfiles_build/media/
