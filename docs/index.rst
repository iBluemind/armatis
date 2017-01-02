=======
Armatis
=======
.. currentmodule:: armatis

Armatis parses the website or web API response of
Korean parcel delivery service company for tracking the parcel.

.. contents::
   :local:
   :backlinks: none


Usage
=====

Armatis is simple to use. Just need to type the delivery company code and the invoice number.

.. code:: python

   tracker = Armatis('cj', 123456789123)
   tracker.find()

The method `find()` returns the dictionary object like below.

.. code:: python

   {
      'company': {
         'contact': '1588-1255',
         'name': 'CJ대한통운'
      },
      'parcel': <armatis.models.Parcel object>,
      'tracks': [
         <armatis.models.Track object>,
         <armatis.models.Track object>,
         <armatis.models.Track object>,
         <armatis.models.Track object>,
         <armatis.models.Track object>,
         <armatis.models.Track object>,
         <armatis.models.Track object>,
         <armatis.models.Track object>,
         <armatis.models.Track object>
      ]
   }

The dictionary has `Parcel` object and `Track` object list.

The **Parcel** object includes the basic information about the parcel delivered.

``sender``
   The name of the person who ships the parcel

``receiver``
   The name of the person who receives the parcel

``address``
   Address of the destination

``note``
   Description about the parcel

``invoice_number``
   The invoice number of the parcel

And, the **Track** object includes the information about the parcel where it was.

``time``
   Status of the delivery history

``status``
   Time of the delivery history

``location``
   Location the parcel where it is

``phone1``
   Contact of the location

``phone2``
   Contact of the location


Supported delivery companies
============================

The following delivery companies are supported currently.
Please contributions for supporting more companies!

+--------------------+----------------+----------------+
| Company            | Test existed   | Last Updated   |
+====================+================+================+
| CJ대한통운         | o              | 2016-12-10     |
+--------------------+----------------+----------------+
| 로젠택배           | o              | 2016-12-10     |
+--------------------+----------------+----------------+
| 현대택배           | o              | 2016-12-10     |
+--------------------+----------------+----------------+
| 한진택배           | o              | 2016-12-10     |
+--------------------+----------------+----------------+
| KG로지스           | o              | 2016-12-10     |
+--------------------+----------------+----------------+
| CVSNet편의점택배   |                | 2014-10-19     |
+--------------------+----------------+----------------+
| GTX로지스          | o              | 2017-01-02     |
+--------------------+----------------+----------------+
| 우체국택배         |                | 2014-10-19     |
+--------------------+----------------+----------------+
| 합동택배           |                | 2014-10-19     |
+--------------------+----------------+----------------+
| EMS                | o              | 2017-01-02     |
+--------------------+----------------+----------------+
| KGB택배            | o              | 2017-01-02     |
+--------------------+----------------+----------------+

You can use the method `supported_companies()` to find the supported delivery company names
and company codes.

.. code:: python

   tracker = Armatis()
   tracker.supported_companies()

`supported_companies()` returns the JSON string like ::

      [
         {
             "code": "lotte",
             "name": "롯데택배"
         },
         {
             "code": "ems",
             "name": "EMS"
         },
         {
             "code": "cvs",
             "name": "CVSNet편의점택배"
         },
         {
             "code": "gtx",
             "name": "GTX로지스"
         },
         {
             "code": "kglogis",
             "name": "KG로지스"
         },
         {
             "code": "kgb",
             "name": "KGB택배"
         },
         {
             "code": "cj",
             "name": "CJ대한통운"
         },
         {
             "code": "hanjin",
             "name": "한진택배"
         },
         {
             "code": "epost",
             "name": "우체국택배"
         },
         {
             "code": "hapdong",
             "name": "합동택배"
         },
         {
             "code": "logen",
             "name": "로젠택배"
         }
      ]


Configuration
=============

You can set global configuration like below.

.. code:: python

   tracker = Armatis('cj', 123456789123,
                     user_agenet='CustomParcelTracker', period=3, validation=True)

Also, this works too.

.. code:: python

   tracker = Armatis('cj', 123456789123,
                     'CustomParcelTracker', 3, True)

`period` is used when `Parser` has an multiple requests.

If you want to check the validation of an invoice number, set `validation` `True`.


How to add new company
======================

You can make the new delivery company parser easily.

First, create a class which inherit `Parser`, and implement the method `parse()`.

.. code:: python

   from armatis.models import Parcel, Track
   from armatis.parser import Parser, ParserRequest

   class NewCompanyParser(Parser):
       def __init__(self, invoice_number, config):
           super(NewCompanyParser, self).__init__(invoice_number, config)
           # Describe the information about the website or web API provided by the delivery company
           parser_request = ParserRequest(url='http://thecompany.co.kr/tracking?invno=%s' % self.invoice_number)
           self.add_request(parser_request)

       # Actually occurred parsing the website or web API provided above
       def parse(self, parser):
           tables = parser.find_all('tbody')

           parcel = Parcel()
           parcel.sender = ...         # Sender's name
           parcel.receiver = ...       # Receiver's name
           parcel.address = ...        # Receive address
           parcel.note = ...           # Describe about the parcel
           self.parcel = parcel        # Store the information about the parcel!

           trs = tables[1].find_all('tr')
           for tr in trs:
               track = Track()
               track.status = ...      # Status of the delivery history
               track.time = ...        # Time of the delivery history
               track.location = ...    # Location the parcel where it is
               track.phone1 = ...      # Contact of the location
               track.phone2 = ...      # Contact of the location
               self.add_track(track)   # Add the tracking information!

If the tracking API has multiple HTTP requests, you can also add multiple requests.

.. code:: python

   ready_request = ParserRequest(url='http://thecompany.co.kr/track'
                                 method='POST',
                                 body='invoice_number=%s' % self.invoice_number,
                                 header={'Content-Type': 'application/x-www-form-urlencoded'})
   self.add_request(ready_request)
   fetch_request = ParserRequest(url='http://thecompany.co.kr/track/result')
   self.add_request(fetch_request)

You can also use list and dictionary!

.. code:: python

   self.requests = [
      {
         'url': 'http://thecompany.co.kr/track',
         'method': 'POST',
         'body': 'invoice_number=%s' % self.invoice_number,
         'header': {'Content-Type': 'application/x-www-form-urlencoded'}
      },
      {
         'url': 'http://thecompany.co.kr/track/result'
      }
   ]

If you have an issue related with character encoding, you can change the character-set like below.

.. code:: python

   class NewCompanyParser(Parser):
      def __init__(self, invoice_number, config):
         config['RESPONSE_ENCODING'] = 'cp949'
         super(NewCompanyParser, self).__init__(invoice_number, config)

And, make a `Company` instance that describe the company.
Finally, register this `Company` object with the `Parser` class you made above.

.. code:: python

   from armatis import Armatis, Company

   tracker = Armatis()

   # Make a Company instance that describe the company
   the_new_company = Company('새로운회사', 'nc', '1234-5678', [10, 12])
   # Register the Company object with the Parser class you made
   tracker.parser_manager.register_parser(the_new_company, NewCompanyParser)

The **Company** object must include the basic information about the delivery company.

``name``
   Company's name

``code``
   Codename

``digit``
   The digit of the invoice number

``phone``
   Phone number of the service center


API Documentation
=================

Tracking a parcel
-----------------

.. module:: armatis

.. class:: Armatis

   .. automethod:: supported_companies

   .. automethod:: find

   .. automethod:: last_result


Registering a new company
-------------------------


.. class:: RequestManager

   .. method:: add_request

      A list of ParserRequest instances


.. class:: ParserRequest

   .. attribute:: url

      API endpoint which can track a parcel

   .. attribute:: method

      HTTP request method

   .. attribute:: body

      The body content for HTTP request

   .. attribute:: header

      The header for HTTP request


.. class:: Parser

   .. attribute:: parcel

      An instance of `Parcel`.

   .. automethod:: parse

   .. automethod:: parser

   .. automethod:: add_track

   .. automethod:: result

   .. method:: find

      Request API and return the result.


.. class:: Company

   .. attribute:: name

      Company's name

   .. attribute:: code

      Codename

   .. attribute:: digit

      The digit of the invoice number

   .. attribute:: phone

      Phone number of the service center


.. class:: Armatis

   .. attribute:: parser_manager

      An instance of `ParserManager`.


.. class:: ParserManager

   .. automethod:: register_parser

