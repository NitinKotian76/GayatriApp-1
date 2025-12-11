dev->staging->prod

dev: --PR-> build images->test-> | 
            |                    |  
            #--master            |  
            |                    |                     
            #--develop           |                     
#--------------------------------|   
|
staging:-- 









develop : develope code
pr : make a pull request
test : test the PR
push : push code to git
build images : build docker images
confirm : confirm deployement
deploy : deploy the code to the server


Test:
    requires all services to be active 
    gayatriapp
    postgresql 
    memcached
    nginx
will run in the local dev environment

staging:
    requires all services to be active 
    gayatriapp
    postgresql 
    memcached
    nginx
will run in a staging server


Deploy:
    requires all services to be active
    postgresql
    memcached
    nginx
    gayatriapp
will run in server prod environment
