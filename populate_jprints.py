import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jprints.settings')
import shutil

import django
django.setup()

from django.conf import settings
from elasticsearch import Elasticsearch
from core.elastic_search import initialise_elastic_search, initialise_pipeline, run_filter, run_agg_filter
from django.contrib.auth.models import User
from core.models import Person, Role, Permission
from publications.models import Publication, Document
from publications.citations import testcitation

def populate_publications():

    test_pubs = [
        {
         "depositor": "admin",
         "status": "I",
         "publication_type": "A",
         "publication_status": "I",
         "visibility_status": "P",
         "title": "Article 1 lorem",
         "abstract": "An abstract for Article 1. Lorem ipsum dolor sit amet, consectetur.",
         "subject": "1",
         "divisions": "1",
         "publication_date": "2017-01-02",
         "document": "test_doc_1.pdf",
         },
         {
         "depositor": "admin",
         "status": "I",
         "publication_type": "A",
         "publication_status": "I",
         "visibility_status": "P",
         "title": "Article 2 ipsum",
         "abstract": "An abstract for Article 2. Lorem ipsum dolor sit amet, consectetur.",
         "subject": "1",
         "divisions": "1",
         "publication_date": "2017-01-02",
         "document": "test_doc_2.pdf",
         },
         {
         "depositor": "admin",
         "status": "I",
         "publication_type": "A",
         "publication_status": "P",
         "visibility_status": "P",
         "title": "Article 3 dolor",
         "abstract": "An abstract for Article 3. Lorem ipsum dolor sit amet, consectetur",
         "subject": "1",
         "divisions": "1",
         "publication_date": "2016-01-02",
         "document": "test_doc_3.pdf",
         },
         {
         "depositor": "test1",
         "status": "I",
         "publication_type": "S",
         "publication_status": "P",
         "visibility_status": "P",
         "title": "Book Section 1 (One)",
         "abstract": "An abstract for Book Section One, note that One is also a family name",
         "subject": "1",
         "divisions": "1",
         "publication_date": "2015-01-02",
         "document": "test_doc_1.odt",
         },
         {
         "depositor": "test2",
         "status": "I",
         "publication_type": "B",
         "publication_status": "S",
         "visibility_status": "P",
         "title": "Book Section 2",
         "abstract": "An abstract for Book Section 2",
         "subject": "1",
         "divisions": "1",
         "publication_date": "2015-01-02",
         "document": "test_doc_1.txt",
         },
         {
         "depositor": "test3",
         "status": "I",
         "publication_type": "B",
         "publication_status": "A",
         "visibility_status": "P",
         "title": "Book accepted",
         "abstract": "An abstract for Book 1 that is accepted",
         "subject": "1",
         "divisions": "1",
         "publication_date": "2015-01-02",
         "document": "test_doc_1.docx",
         },
          {
         "depositor": "test3",
         "status": "I",
         "publication_type": "B",
         "publication_status": "S",
         "visibility_status": "P",
         "title": "Book submitted",
         "abstract": "An abstract for Book 1 that is submitted",
         "subject": "1",
         "divisions": "1",
         "publication_date": "2015-01-02",
         },
   
   ]

    for i in range(25):
        test_pubs.append(
          {
            "depositor": "test3",
            "status": "A",
            "publication_type": "A",
            "publication_status": "I",
            "visibility_status": "P",
            "title": "Test Article "+str(i),
            "abstract": "An abstract for test article "+str(i)+" that is published",
            "subject": "1",
            "divisions": "1",
            "publication_date": "2017-01-02",
          },
        )

    for pub in test_pubs:
        add_publication(pub)

def add_publication(pub):
    print("add publication: depositor {0} type {1} title {2}".format(str(pub["depositor"]), str(pub["publication_type"]), str(pub["title"])))
    u = User.objects.get_or_create(username=pub["depositor"])[0]
    person = Person.objects.get_or_create(user=u)[0]
    p = Publication.objects.get_or_create(depositor=person, title=pub["title"])[0]
    p.status = pub["status"]
    p.publication_type = pub["publication_type"]
    p.publication_status = pub["publication_status"]
    p.visibility_status = pub["visibility_status"]
    p.abstract = pub["abstract"]
    p.subject = pub["subject"]
    p.divisions = pub["divisions"]
    p.publication_date = pub["publication_date"]
    #p.online_date = pub["online_date"]
    #p.accept_date = pub["accept_date"]
    #p.submit_date = pub["submit_date"]
    #p.complete_date = pub["complete_date"]

    if ( "document" in pub ):
        d = Document.objects.get_or_create(publication=p)[0]
        d.save()
        src_path = settings.STATIC_DIR + "/testdoc/"+pub["document"]
        doc_path = "pub/"+str(p.id)+"/doc/"+str(d.id)+"/"
        doc_name = pub["document"]
        dest_path = settings.MEDIA_DIR +"/"+ doc_path
        os.makedirs(dest_path)
        shutil.copy(src_path, dest_path+doc_name)
        print("Pub doc", "src", src_path, "dest", dest_path)
        d.filefield.name = doc_path+doc_name

        d.save()
    p.save()

def populate_people():

    test_users = [
        {"username": "admin",
         "email": "pjw@drserv.org",
         "first": "Peter",
         "last": "West",
         "staff": "Yes",
         "disp_title": "Mr",
         "disp_given": "Peter",
         "disp_family": "West",
         "lang": "EN",
         "orcid": "0000-0002-0244-9026",
         "user_type": "Ad",
         "dept": "dept 1",
         "org": "org 1",
         "addr": "here and there",
         },
    
        {"username": "test1",
         "email": "test@test1.com",
         "first": "Test",
         "last": "One",
         "staff": "No",
         "disp_title": "Mr",
         "disp_given": "Test",
         "disp_family": "One",
         "lang": "EN",
         "orcid": "1234-1234-1234-1234",
         "user_type": "Us",
         "dept": "dept 1",
         "org": "org 1",
         "addr": "here and there",
         "photo": "default_male_128.png",
         },
         {"username": "test2",
         "email": "test@test2.com",
         "first": "Test",
         "last": "Two",
         "staff": "No",
         "disp_title": "Mrs",
         "disp_given": "Test",
         "disp_family": "Two",
         "lang": "DE",
         "orcid": "0000-1234-0002-0002",
         "user_type": "Us",
         "dept": "dept 1",
         "org": "org 1",
         "addr": "here and there",
         "photo": "default_female_128.png",
         },
         {"username": "test3",
         "email": "test@test3.com",
         "first": "Test",
         "last": "Three",
         "staff": "No",
         "disp_title": "Miss",
         "disp_given": "dispgiven",
         "disp_family": "",
         "lang": "DE",
         "orcid": "0000-1234-0002-0002",
         "user_type": "Us",
         "dept": "dept 1",
         "org": "org 1",
         "addr": "here and there",
         "photo": "default_female_128.png",
         },
    ]

    for user in test_users:
        add_user(user)

def add_user(user):
    print("add user: {0} {1} {2}".format(str(user["username"]), str(user["first"]), str(user["last"])))
    u = User.objects.get_or_create(username=user["username"], email=user["email"], first_name=user["first"], last_name=user["last"])[0]
    u.set_password("pypuser1")
    u.save()
    p = Person.objects.get_or_create(user=u)[0]
    p.disp_title = user["disp_title"]
    p.disp_given = user["disp_given"]
    p.disp_family = user["disp_family"]
    p.lang = user["lang"]
    p.orcid = user["orcid"]
    p.user_type = user["user_type"]
    p.dept = user["dept"]
    p.org = user["org"]
    p.addr = user["addr"]

    p.save()
    if ( "photo" in user ):
        src_path = settings.STATIC_DIR + "/images/"+user["photo"]
        photo_path = "profile/"+str(p.id)+"/photo/"
        #photo_path = "/profile/"+str(p.id)+"/photo/"
        photo_name = "userphoto.png"
        dest_path = settings.MEDIA_DIR + "/" +photo_path
        os.makedirs(dest_path)
        shutil.copy(src_path, dest_path+photo_name)
        print("User photo", "src", src_path, "dest", dest_path)
        p.photo.name = photo_path+photo_name

        p.save()


def clear_database():
    publications = Publication.objects.order_by('id')
    for publication in publications:
        print("About to delete publication ",publication.id,publication.title)
        publication.delete()

    people = Person.objects.order_by('id')
    for person in people:
        if person.user_type != "Ad":
            print("deleting person ",person.id,person.disp_family)
            person.delete()
        else:
            print("Not deleting person ",person.id,person.disp_family)


    users = User.objects.order_by('id')
    for user in users:
        if user.is_staff != True:
            print("deleting user ", user.id, user.last_name, user.is_staff)
            user.delete()


if __name__ == '__main__':
    print("clear database")
    clear_database()

    print("Setup Elastic Search indexes")
    initialise_elastic_search()

    print("Setup Elastic Search ingest pipeline")
    initialise_pipeline()

    print("Start populate JPrints")
    populate_people()
    populate_publications()

    #run_filter( "publication", "item_type", "A" )
    #run_filter( "publication", "item_type", "B" )
    #run_agg_filter( "publication", {}, {} )
    #run_agg_filter( "person", {}, {} )

    testcitation()

    print("Finished JPrints population script")
