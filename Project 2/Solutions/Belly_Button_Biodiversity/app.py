import os
import json
import pandas as pd
import numpy as np
import psycopg2
import psycopg2.extras
import sys


from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


#################################################
# Database Setup
#################################################
conn_string = "host='localhost' dbname='ETL' user='etl' password='etl'"
print ("Connecting to database\n	->%s" % (conn_string))
 
conn = psycopg2.connect(conn_string)
 
	
dict_cur = conn.cursor('cursor_unique_name', cursor_factory=psycopg2.extras.DictCursor)
dict_cur.execute('SELECT * FROM cleaned1_data')
rec= dict_cur.fetchall()
# print(rec[0])

	
@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")



@app.route("/names")
def names():
   
   
   row_count =0 
   country_list=[]
   # dict={}
   for row_count in range(len(rec)):
      country_list.append(rec[row_count][1])
      # print(country_list[row_count])
      row_count += 1
   # dict={"country":country_list}
   return(jsonify(country_list))
   # return(dict)



# @app.route("/metadata/<sample>")
# def sample_metadata(sample):
#     """Return the MetaData for a given sample."""
#     # sel = [
#     #     Samples_Metadata.sample,    
#     #     Samples_Metadata.ETHNICITY,
#     #     Samples_Metadata.GENDER,
#     #     Samples_Metadata.AGE,
#     #     Samples_Metadata.LOCATION,
#     #     Samples_Metadata.BBTYPE,
#     #     Samples_Metadata.WFREQ,
#     # ]

# #     results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

#     # Create a dictionary entry for each row of metadata information
#     # sample_metadata = {}
#     # for record in records:
#     #     sample_metadata["Country"] = record[0]
#     #     sample_metadata["Family"] = record[1]
#     #     sample_metadata["Freedom"] = record[2]
#     #     sample_metadata["Generosity"] = record[3]
#     #     sample_metadata["Happiness Rank"] = record[4]
#     #     sample_metadata["Happiness Score"] = record[5]
#     #     sample_metadata["Year"] = record[6]

#     # print(sample_metadata)
#     # return jsonify(sample_metadata)


@app.route("/samples/<sample>")
def samples(sample):
    """Return `otu_ids`, `otu_labels`,and `sample_values`."""
   
    count =0 
    Fertility_rate=[]
    happines_score=[]
    country=[]
    dict={}
   #  print(sample)
    for count in range(len(rec)):
      if rec[count][1]==sample:
         # print("hello")
         Fertility_rate.append(rec[count][19])
         happines_score.append(rec[count][6])
         country.append(rec[count][1])
         print(Fertility_rate[0])
    count += 1
    dict={"Fertility":Fertility_rate,
          "Happines_score":happines_score,
          "Country":country}
   #  return(jsonify(country_list))
    return(jsonify(dict))
    # Format the data to send as json
   #  data = {
   #      "otu_ids": sample_data.otu_id.values.tolist(),
   #      "sample_values": sample_data[sample].values.tolist(),
   #      "otu_labels": sample_data.otu_label.tolist(),
   #  }
   #  return jsonify(data)


if __name__ == "__main__":
    app.run()
