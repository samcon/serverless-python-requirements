import os
import shutil
import sys
import zipfile

pkgdir = '/tmp/sls-py-req'

# We want our path to look like [working_dir, serverless_requirements, ...]
sys.path.insert(1, pkgdir)

if not os.path.exists(pkgdir):
    tempdir = '/tmp/_temp-sls-py-req'
    if os.path.exists(tempdir):
        shutil.rmtree(tempdir)

    default_lambda_task_root = os.environ.get('LAMBDA_TASK_ROOT', os.getcwd())
    lambda_task_root = os.getcwd() if os.environ.get('IS_LOCAL') == 'true' else default_lambda_task_root
    zip_requirements = os.path.join(lambda_task_root, '.requirements.zip')

    zipfile.ZipFile(zip_requirements, 'r').extractall(tempdir)

    zip_requirements_layer_reqs = os.path.join('/opt/', '.requirements.zip')
    if os.path.isfile(zip_requirements_layer_reqs):
        zipfile.ZipFile(zip_requirements_layer_reqs, 'r').extractall(tempdir)

    os.rename(tempdir, pkgdir)  # Atomic
