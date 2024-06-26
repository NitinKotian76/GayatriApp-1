from marshmallow import Schema,fields
from dataclasses import dataclass
from pprint import pprint

@dataclass
class form:
    author:str
    formData:str
    
class datastore(Schema):
    author = fields.Str()
    formData = fields.Str()

# def appendfields():

# def selectField():


    # <script>
    #     $(function() {
    #         $('.addBtn').click(function(){
    #             $.ajax({
    #                 url: "{% url 'samples' %}",
    #                 success: function(data){
    #                     return data;
    #                 }
    #             });
    #         });
    #     });
    # </script>
