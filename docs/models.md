---
title: "Model Architecture Planning"
output: "pdf_document"
---

# Model Architecture Planning


## I- user Model
##### Fields
* username: String
* first_name: String
* last_name: String
* email: email
* password: String
* is_staff
* is_active
* last_login: datetime
* date_joined: datetime
##### Attribute
* is_authenticated
##### Methods
*-- get_username()*
*-- get_full_name()*
*-- get_short_name()*
*-- set_password(raw_password)*
*-- check_password(raw_password)*
*-- email_user(subject, message, from_email=None, \*\*kwargs)*

## II- SuperUser Model (*user*)
##### Fields
* slug: Slug *
* stripe_customer_id = models.CharField(max_length=40)
* language             (In the parameters)
* profile picture
* course list          (list of Pks of the user courses)
* links:
    * Website_url
    * twitter: http://www.twitter.com/Username
    * facebook: http://www.facebook.com/Username
    * linkedin: http://www.linkedin.com/ResourceID
    * youtube: http://www.youtube.com/Username

## III- Tutor Model (*SuperUser*)
##### Fields
* Title
* membership = models.ForeignKey( Membership, on_delete=models.    SET_NULL, null=True)
* Biography
* Study * 
    * options

## IV- Student Model (*SuperUser*)
##### Fields
None

## III- Course Model
##### Fields
* slug 
* title * 
* summary *
* picture 
* description *
* objectives *
* Category *
    * Development
    * Business
    * IT & Software 
    * ...
* level *
    * beginner
    * Intermidiate
    * Advanced
* price *
* discount
* avg rating
* total duration
* number of courses
* owner (Foreign Key to *Tutor*)

## Lesson Model
##### Fields
* slug  
* Course (foreignkey to *Course*) 
* position *
* title * #Introduction
* video *


## Feedback Model 
##### Fields

* message *
* rating (out of 5) 
* user (Foreign Key to *Student*)
* course (Foreign Key to *Course*)

## Comment Model 
##### Fields
* message *
* user (Foreign Key to *SuperUser*)
* lesson (Foreign Key to *Lesson*)

## Reply Model 
##### Fields
* message *
* comment (Foreign Key to *Comment*)
* user (Foreign Key to *SuperUser*)

## Tracking Model
##### Fields
* lesson (foreignkey to *Lesson*) 
* student (foreignkey to *Student*) 
* duration 




## Tracking table example                       
    #id     #lesson id     #student_id   #watched   #total_duration
    1       id 1           cheick        3.454      4.32
    2       id1            victor        6.32       7.12
    3       id1            x             3          9.62
    4       id2            cheick        8.12       8.12
    5       id2            victor        4.65       5.939