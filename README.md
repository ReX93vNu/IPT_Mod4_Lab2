# IPT_Mod4_Lab2
by a potato

Reusing the old Mod4_lab1 activity by simply adding a payment api for tuition scenarios.

A Lab activity to satisfy the following:

Problem Scenario 
You are building a Secure Payment API that handles sensitive user information. 

The system must be able to.
● Encrypt sensitive fields.

Encypted credit card info:
<img width="921" height="329" alt="image" src="https://github.com/user-attachments/assets/32c32c3d-abfa-433b-8b3d-96ed7f0918da" />

● Hash passwords securely.

Hashed user password with argon2:
<img width="900" height="296" alt="image" src="https://github.com/user-attachments/assets/06947b40-a15f-4fb8-a399-f5f14e762b32" />

● Prevent brute-force attacks.

first login attempt without auth:
![alt text](image-1.png)

login attempt with pass and user:
![alt text](image-6.png)

after multiple attempts:
![alt text](image-5.png)
![alt text](image-7.png)

succesful logins:
user & pass
![alt text](image-8.png)

token. error 400 appears because no payload was delivered, but login is sucessful as we didnt get a 401 error.
![alt text](image-9.png)


● Log security-related events.
log of multiple attempted logins:
![alt text](image-12.png)


Students must test.
● Access without authentication. Done up top
● Excessive API requests. Done up top

● Invalid encrypted payloads.
when sending an invalid encrypted data:
![alt text](image-11.png)

when sending valid encrypted data:
![alt text](image-10.png)

