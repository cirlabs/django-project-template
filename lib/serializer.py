"""
Tastypie serializer class for CSV exports and pretty priting JSON

Note: This code won't work out the box.
Use it as a starting point for other custom serializers in a project
"""
import csv
import json

from django.http import HttpResponse
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
        return json.dumps(
            data,
            cls=DjangoJSONEncoder,
            sort_keys=True,
            ensure_ascii=False,
            indent=self.json_indent
        )

    def to_csv(self, data, options=None):
        """
        Given some Python data, produces JSON output.

        """
        response = HttpResponse()

        options = options or {}
        data = self.to_simple(data, options)
        writer = csv.writer(response)
        writer.writerow(data[0].keys())

        for item in data:
            keys = item.keys()
            writer.writerow([self.encode(item, key) for key in keys])

        return response

    def encode(self, aitem, akey):
        return unicode(aitem[akey]).encode('utf-8', 'replace')
