import os

#docker run build

# Build consult-db-slave
os.system("cd ./consult-db-slave && docker build -t consult-db-slave .")

# Build load-balancer
os.system("cd ./load-balancer && docker build -t load-balancer .")
