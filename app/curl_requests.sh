#curl --header "Content-Type: application/json" \
#--request POST --data '{"username" : "luq", "email": "luq@wp.pl", "password": "password"}' \
#http://localhost:5000/api/v1/auth/register

#curl --header "Content-Type: application/json" \
#--request POST --data '{"username" : "luq", "email": "luq@wp.pl", "password": "password"}' \
#http://localhost:5000/api/v1/auth/login


curl --header "Content-Type: application/json" --request POST --data '{"email": "luq@wp.pl"}' http://localhost:5000/api/v1/bookmarks/add_todo
