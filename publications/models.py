from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

import json

from core.elastic_search import index_publication

class Milestone(models.Model):
    MILESTONE_TYPES = (
        ( 'D', _('Deposited') ),
        ( 'L', _('Live') ),
        ( 'A', _('Accepted') ),
        ( 'P', _('Published') ),
    )
 
    date = models.DateTimeField()
    milestone_type = models.CharField(max_length=1, choices=MILESTONE_TYPES)

DOCUMENT_TYPES = (
        ( 'dra', _('draft') ),
        ( 'sub', _('submitted') ),
        ( 'acc', _('accepted') ),
        ( 'pub', _('published') ),
        ( 'upd', _('updated') ),
        ( 'sup', _('supplemental') ),
        ( 'cov', _('coverimage') ),
        ( 'dat', _('dataset') ),
        ( 'pre', _('presentation') ),
        ( 'oth', _('other') ),
    )

LICENCES = (
        ( 'publi', 'publisher' ),
        ( 'cc_by', 'cc_by' ),
        ( 'by_nc', 'cc_by_nc' ),
        ( 'by_nd', 'cc_by_nd' ),
        ( 'nc_nd', 'cc_by_nc_nd' ),
        ( 'nc_sa', 'cc_by_nc_sa' ),
        ( 'by_sa', 'cc_by_sa' ),
        ( 'cc_pd', 'cc_public_domain' ),
    )

VISIBILITY_STATES = (
        ( 'P', _('Public') ),
        ( 'R', _('Restricted') ),
        ( 'E', _('Embagoed') ),
        ( 'N', _('None') ),
    )



class Publication(models.Model):
    from core.models import Person

    PUBLICATION_TYPES = (
        ( 'A', _('Article') ),
        ( 'B', _('Book') ),
        ( 'S', _('Book Section') ),
    )

    STATUS_TYPES = (
        ( 'I', _('inbox') ),
        ( 'B', _('buffer') ),
        ( 'A', _('archive') ),
        ( 'D', _('deletion') ),
    )

    PUBLICATION_STATES = (
        ( 'S', _('Submitted') ),
        ( 'A', _('Accepted') ),
        ( 'P', _('Published') ),
        ( 'I', _('In Press') ),
        ( 'U', _('Unpublished') ),
    )

    VISIBILITY_STATES = (
        ( 'P', _('Public') ),
        ( 'R', _('Restricted') ),
        ( 'E', _('Embagoed') ),
        ( 'N', _('None') ),
    )

    # metadata fields
    depositor = models.ForeignKey(Person)
    contributors = models.ManyToManyField(Person, related_name='contributes_to', through='Contributor')

    status = models.CharField(max_length=1, choices=STATUS_TYPES, default='I')
    publication_type = models.CharField(max_length=1, choices=PUBLICATION_TYPES, default='A')
    publication_status = models.CharField(max_length=1, choices=PUBLICATION_STATES, default='U')
    visibility_status = models.CharField(max_length=1, choices=VISIBILITY_STATES, default='N')
    title = models.CharField(max_length=200, blank=True)
    abstract = models.TextField(blank=True)

    publication_date = models.DateField(auto_now=False,auto_now_add=False,blank=True)
    online_date = models.DateField(null=True,auto_now=False,auto_now_add=False,blank=True)
    accept_date = models.DateField(null=True,auto_now=False,auto_now_add=False,blank=True)
    submit_date = models.DateField(null=True,auto_now=False,auto_now_add=False,blank=True)
    complete_date = models.DateField(null=True,auto_now=False,auto_now_add=False,blank=True)

    subject = models.CharField(max_length=200, blank=True)
    divisions = models.CharField(max_length=200, blank=True)
    
    keywords = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    suggestions = models.TextField(blank=True)
    book_series = models.CharField(max_length=200, blank=True)
    journal = models.CharField(max_length=200, blank=True)
    volume = models.CharField(max_length=200, blank=True)
    issue = models.CharField(max_length=200, blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    place_of_pub = models.CharField(max_length=200, blank=True)
    pagerange = models.CharField(max_length=200, blank=True)
    pages = models.CharField(max_length=200, blank=True)
    issn_e = models.CharField(max_length=200, blank=True)
    issn_p = models.CharField(max_length=200, blank=True)
    issn_l = models.CharField(max_length=200, blank=True)
    isbn = models.CharField(max_length=200, blank=True)
    book_title = models.CharField(max_length=200, blank=True)
    doi = models.CharField(max_length=200, blank=True)
    pubmedid = models.CharField(max_length=200, blank=True)
    wosid = models.CharField(max_length=200, blank=True)

    revision = models.IntegerField(default=1, editable=False)
    created = models.DateTimeField(auto_now_add=True, )
    #created = models.DateTimeField(auto_now_add=True, default=timezone.now(), editable=False)
    lastmod = models.DateTimeField(auto_now=True, blank=True, editable=False)

    def index(self):
        index_publication( self )

    # override the save method to index the object in elastic search
    def save(self, *args, **kwargs):
        super(Publication, self).save(*args, **kwargs) 
        index_publication( self )

    def get_publication_type_str(self):
        type = ""
        if (self.publication_type):
            for t,n in Publication.PUBLICATION_TYPES:
                if ( t == self.publication_type ):
                    return n
        return type

    def get_search_citation(self):
        citation = self.title+" ["+self.get_publication_type_str()+"] "+self.abstract
        return citation

    def get_icon_name(self):
        icon_name = "research_books.png"
        if ( self.publication_type == "A" ):
            icon_name = "doc_file.png"
        elif ( self.publication_type == "B" ):
            icon_name = "research_books.png"
        elif ( self.publication_type == "S" ):
            icon_name = "research_books.png"

        return icon_name

    def get_choice_disp_str( the_choices, key ):
        disp = key
        for t,n in the_choices:
            if ( t == key ):
                return n
        return disp

    def get_json_citation(self):
        authors = []
        authors.append( { "family": "Grignon", "given": "Cyril" })
        citation = { 
            'id': str(self.id),
            'title': self.title,
            'type': self.get_publication_type_str(),
            'author': authors,
            'publisher-place': "London",
            'publisher': "A Publisher",
            'URL': "http://publisher.id",
            'page': "120-124"
        }

        if self.publication_date:
            cit_issued_date_val = []
            cit_issued_date_val.append(self.publication_date.year)
            if self.publication_date.month:
                cit_issued_date_val.append( self.publication_date.month )
            if self.publication_date.day:
                cit_issued_date_val.append( self.publication_date.day )
            cit_issued_date = []
            cit_issued_date.append(cit_issued_date_val)
        
            cit_issued = { "date-parts": cit_issued_date }
            citation['issued'] = cit_issued

        return json.dumps( citation ) 


    def __str__(self):
        return '%s %s' % (self.id, self.title)





class Document(models.Model):

    def pub_doc_path(instance, filename):
        return 'pub/{0}/doc/{1}/{2}'.format(instance.publication.id, instance.id, filename)

    publication = models.ForeignKey('Publication', on_delete=models.CASCADE)

    doc_type = models.CharField(max_length=3, choices=DOCUMENT_TYPES, default='dra')
    visibility_status = models.CharField(max_length=1, choices=VISIBILITY_STATES, default='N')
    licence = models.CharField(max_length=5, choices=LICENCES, blank=True) 
    embargo = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, )
    filefield = models.FileField(upload_to=pub_doc_path, blank=True)



class Contributor(models.Model):
    from core.models import Person

    CONTRIBUTION_TYPES = (
        ( 'Au', _('Author') ),
        ( 'Ed', _('Editor') ),
        ( 'Ad', _('Advisor') ),
        ( 'Re', _('Referee') ),
        ( 'Tr', _('TRANSLATOR') ),
    )
 
    contribution_type = models.CharField(max_length=2, choices=CONTRIBUTION_TYPES)
    person = models.ForeignKey(Person)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(default=1)



