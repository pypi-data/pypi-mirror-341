# Insafe Connect to Database

### Build library command
`python setup.py sdist bdist_wheel`

### Upload library command
`twine upload dist/*`

### Install specific version
pip install insafeConnectToDatabase==0.2.2



### Database Connection issue
while trying to connect to dataase we faced multiple issues as the following
- connect to staging database with proxy
  - we should use the library which going to install the proxy script and read service account from env
- have conflict with prot number 4532 which is shared between postrgress we have in the cloud and the one we
have in local docker
  - we have to change one of the port numbers