# autodestroymessage
Auto Destroy Message after Reading

## Features
* Creates Encrypted Messages.
* Unique hashed URL is provided on message creation.
* The message self destroy itself after reading from the user.
* Even if the DB security is compromised, no one will be able to access the message which is send to other user as everything is encrypted.
* When the message is read, we deletes the message and save the IP address of the user and the time of reading the note.