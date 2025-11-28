develop -> PR -> test -> push -> build images -> confirm -> deploy
^                    |              |
|___________________ V              #--master
                                    |
                                    #--develop
develop : develope code
pr : make a pull request
test : test the PR
push : push code to git
build images : build docker images
confirm : confirm deployement
deploy : deploy the code to the server


Test:
    requires all services to be active 
    postgresql 
    memcached
    nginx
will run in the local dev environment

Deploy:
    requires all services to be active
    postgresql
    memcached
    nginx
    gayatriapp
will run in server prod environment
