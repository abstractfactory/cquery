.. _overview:

Schemaless
==========

cQuery for schemaless directory structures

Why Schemaless?
---------------

cQuery doesn't solve the issues surrounding data-modeling. When defining a :term:`schema`, you map a digital landscape onto metaphors more easily understood than their digital counterpart. You then build tools upon this map, with the intent that the landscape rarely, ideally never, changes. Although this works and has worked for a long time, change is inevitable and schemas simply doesn't cope all that well with it - i.e. a change to a schema, depending on its magnitude, may well break your tools.

Again, cQuery doesn't solve this issue, data-modeling is inherently a human problem, not a technical one. What cQuery does however is move the barrier at which change starts to affect the work you build upon it so that you are free to start building long before you know how your digital landscape will end up looking.

Generally, there is a direct analogy between a schemaless style and dynamically typed languages. And as with such languages, it is extra important to explicitly document the definition, motivation and purpose of each decision made. What cQuery allows you to do is to move this decision-making process onto a later stage. As they say, procrastination leads to wiser decisions.

See also
    - `Data and Reality, Kent`_
    - `Managing Data in Motion, Reeve`_
    - `Data Modeling Essentials, 3rd ed., Graeme`_
    - http://martinfowler.com/articles/schemaless/

Motivation
----------

Traditionally, prior to commencing a new project, you would spend a little time on figuring out an appropriate directory structure to encapsulate the data this project will generate. Something like:

.. code-block:: bash

    o project
      o- assets
         o- peterparker
         o- loislane
      o- shots
         o- 1000
         o- 2000
         o- 3000
         o- 4000

Upon which you then set out to build your tools. But what if your next project also features sequences, or levels? What if the hierarchy is located on a Unix-drive or a network share depending on which computer accesses the data? The number of variables upon venturing out on any projects can never be assumed and will continuously change and the work you build on-top will have to facilitate this change.

.. _Data and Reality, Kent: http://www.amazon.co.uk/Data-Reality-Perspective-Perceiving-Information/dp/1935504215
.. _Data Modeling Essentials, 3rd ed., Graeme: http://www.amazon.co.uk/Modeling-Essentials-Kaufmann-Management-Systems/dp/0126445516/ref=sr_1_1?s=books&ie=UTF8&qid=1403708358&sr=1-1&keywords=Data+Modeling+Essentials
.. _Managing Data in Motion, Reeve: http://www.amazon.co.uk/Managing-Data-Motion-Technologies-Intelligence/dp/0123971675/ref=sr_1_1?s=books&ie=UTF8&qid=1403708380&sr=1-1&keywords=Managing+Data+in+Motion