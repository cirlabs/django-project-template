"""
Tastypie serializer class for CSV exports and pretty priting JSON

Note: This code won't work out the box.
Use it as a starting point for other custom serializers in a project
"""
import csv
import json
from django.http import HttpResponse
from django.utils.datastructures import SortedDict
from django.core.serializers.json import DjangoJSONEncoder
from tastypie.serializers import Serializer

class CIRCustomSerializer(Serializer):
    json_indent = 2
    formats = Serializer.formats + ['csv']
    content_types = dict(
        Serializer.content_types.items() + [('csv', 'text/csv')]
    )

    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        return json.dumps(data, cls=DjangoJSONEncoder,
                sort_keys=True, ensure_ascii=False, indent=self.json_indent)

    def to_csv(self, data, options=None):
        """
        Given some Python data, produces JSON output.

        """
        response = HttpResponse()

        options = options or {}
        data = self.to_simple(data, options)

        csv_data = self.construct_data(data)
        writer = csv.writer(response)

        # 12 is semi-arbitray, it just means it's not single decade of data so
        # it's probably a bulk export
        if len(csv_data) > 12:
            # bulk object
            writer.writerow(csv_data[0][0].keys())
            for data in csv_data:
                for item in data:
                    writer.writerow([unicode(item[key]).encode('utf-8', 'replace') for key in item.keys()])
        else:
            # single object
            writer.writerow(csv_data[0].keys())
            for item in csv_data:
                writer.writerow([unicode(item[key]).encode('utf-8', 'replace') for key in item.keys()])

        return response

    def construct_data(self, data):
        if 'objects' in data:
            data_export = []
            for item in data['objects']:
                data_export.append(self.create_dict(item))

            return data_export
        else:
           return self.create_dict(data)

    def _filter(self, dictlist, key, valuelist):
      return [dictio for dictio in dictlist if dictio[key] in valuelist]

    def create_dict(self, data):
        try:
            data_export = []

            years = range(2001, 2013) #2001-2012
            for year in years:
                row = SortedDict()
                # name
                row['name'] = data['name']
                # set year
                row['year'] = year
                # add city and state if they exit
                if 'hq_city' in data:
                    row['city'] = data['hq_city']

                if 'hq_state' in data:
                    row['state'] = data['hq_state']

                if 'city' in data:
                    row['city'] = data['city']

                if 'state' in data:
                    row['state'] = data['state']

                if 'region' in data:
                    row['region'] = data['region']['name']

                if 'system' in data:
                    row['system'] = data['system']['name']

                # grab total data
                stat = self._filter(data['stats']['all_drugs_years'], 'year', [year])[0]

                row['total_patients'] = stat['patients']
                row['total_prescription_count'] = stat['scrip_cnt']
                row['all_opiate_prescriptions_per_100_patients'] = stat['scrip_rate']

                # iterate through four drugs
                for drug in data['stats']['drugs']:
                    # filter for data of drug and year
                    stat = self._filter(drug['years'], 'year', [year])[0]

                    row[drug['drug'].lower()] = stat['scrip_cnt']

                # notes about the data
                if 'notes' in data:
                    row['notes'] = data['notes']

                data_export.append(row)

            return data_export
        except KeyError, e:
            print "Error: ", e
            pass
