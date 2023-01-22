import unittest
import fastapifunc
import os


class TestEmployee(unittest.TestCase):

    def setUp(self):
        csvFilePath = r'MadaReports.csv'
        jsonFilePath = r'jason.json'
        jsonArray = main.csv_to_json(csvFilePath, jsonFilePath)
        return jsonArray

    def test_json_correct(self):
        jsonArray = self.setUp()
        self.assertEqual(jsonArray['testuser']['IDNum'], '878746593')
        self.assertEqual(jsonArray['testuser']['IDType'], '0')
        self.assertEqual(jsonArray['testuser']['FirstName'], 'Garfield')
        self.assertEqual(jsonArray['testuser']['LastName'], 'Sapseed')
        self.assertEqual(jsonArray['testuser']['City'], 'Sinacaban')
        self.assertEqual(jsonArray['testuser']['Street'], 'Mockingbird')
        self.assertEqual(jsonArray['testuser']['BuildingNumber'], '36')
        self.assertEqual(jsonArray['testuser']['Barcode'], '21ABBA1C-1292-5EB2-0BBA-7C4AB5DB1185')
        self.assertEqual(jsonArray['testuser']['GetDate'], '28.04.2021')
        self.assertEqual(jsonArray['testuser']['TakeDate'], '04.07.2021')
        self.assertEqual(jsonArray['testuser']['ResultDate'], '23/03/2021')

    def test_json_empty(self):
        jsonArray = self.setUp()
        self.assertEqual(jsonArray['empty_BuildingNumber_Barcode']['BuildingNumber'], '')
        self.assertEqual(jsonArray['empty_BuildingNumber_Barcode']['Barcode'], '')

    def test_csvfile_exists_csv(self):
        csvFilePath = r'MadaReports.csv'
        self.assertTrue(os.path.isfile(csvFilePath))
        self.assertTrue(csvFilePath.endswith('.csv'))

    def test_jsonfile_exists_json(self):
        jsonFilePath = r'jason.json'
        self.assertTrue(os.path.isfile(jsonFilePath))
        self.assertTrue(jsonFilePath.endswith('.json'))






if __name__ == '__main__':
    unittest.main()