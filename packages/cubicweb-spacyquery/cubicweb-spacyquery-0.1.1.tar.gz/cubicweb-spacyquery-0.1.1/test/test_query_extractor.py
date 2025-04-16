from unittest import TestCase

import tempfile
from pathlib import Path

from utils import generate_schema_data
from cubicweb_spacyquery.query_extractor import QueryExtractor

import pandas as pd


with tempfile.TemporaryDirectory() as tmpdirname:
    _, _, rfile = generate_schema_data(Path(tmpdirname))
    relations = pd.read_csv(rfile, sep=";")
    QE = QueryExtractor(relations)


class QueryExtractorTC(TestCase):

    def test_only_one_etype(self):
        query = QE.get_queries(["Person"], [])
        expected = "Any PERSON WHERE PERSON is Person"
        self.assertEqual(query, expected)

    def test_simple_entity_link(self):
        query = QE.get_queries(["Person", "Organization"], [])
        expected = (
            "Any ORGANIZATION, PERSON WHERE ORGANIZATION is Organization,"
            " PERSON is Person, PERSON works_for ORGANIZATION"
        )
        self.assertEqual(query, expected)

    def test_simple_entity_link_and_attr(self):
        query = QE.get_queries(
            ["Person", "Organization"], ["Person#firstname", "Organization#name"]
        )
        expected = (
            "Any PERSON_FIRSTNAME, ORGANIZATION_NAME, ORGANIZATION,"
            " PERSON WHERE PERSON firstname PERSON_FIRSTNAME,"
            " ORGANIZATION name ORGANIZATION_NAME, ORGANIZATION"
            " is Organization, PERSON is Person,"
            " PERSON works_for ORGANIZATION"
        )
        self.assertEqual(query, expected)

    def test_simple_entity_link_and_multi_attr(self):
        query = QE.get_queries(
            ["Person", "Organization"],
            ["Person#firstname", "Person#lastname", "Organization#name"],
        )
        expected = (
            "Any PERSON_FIRSTNAME, PERSON_LASTNAME, ORGANIZATION_NAME,"
            " ORGANIZATION, PERSON WHERE PERSON firstname PERSON_FIRSTNAME,"
            " PERSON lastname PERSON_LASTNAME, ORGANIZATION name"
            " ORGANIZATION_NAME, ORGANIZATION is Organization, PERSON is Person,"
            " PERSON works_for ORGANIZATION"
        )
        self.assertEqual(query, expected)

    def test_missing_entity_link_and_attr(self):
        query = QE.get_queries(
            ["Person"],
            ["Person#firstname", "Organization#name"],
        )
        expected = (
            "Any PERSON_FIRSTNAME, ORGANIZATION_NAME, PERSON, ORGANIZATION"
            " WHERE PERSON firstname PERSON_FIRSTNAME, ORGANIZATION name"
            " ORGANIZATION_NAME, PERSON is Person, ORGANIZATION is"
            " Organization, PERSON works_for ORGANIZATION"
        )
        self.assertEqual(query, expected)

    def test_first(self):
        query = QE.get_queries(["Person", "SubComponent"], [])
        expected = (
            "Any SUBCOMPONENT, COMPONENT, PROJECT, PERSON WHERE SUBCOMPONENT"
            " is SubComponent, COMPONENT is Component, PROJECT is Project,"
            " PERSON is Person, COMPONENT has_subcomponent SUBCOMPONENT,"
            " PROJECT includes COMPONENT, PROJECT involves PERSON"
        )
        self.assertEqual(query, expected)

    def test_second(self):
        query = QE.get_queries(["Person", "Theme"], [])
        expected = (
            "Any THEME, DOCUMENT, PERSON WHERE THEME is Theme, DOCUMENT"
            " is Document, PERSON is Person, DOCUMENT relates_to THEME,"
            " PERSON writes DOCUMENT"
        )
        self.assertEqual(query, expected)

    def test_simple_entity_link_and_attr_value(self):
        query = QE.get_queries(
            ["Person", "Organization"],
            ["Person#firstname", "Organization#name#Lglb"],
        )
        expected = (
            "Any PERSON_FIRSTNAME, ORGANIZATION, PERSON WHERE PERSON firstname"
            " PERSON_FIRSTNAME, ORGANIZATION is Organization, ORGANIZATION name"
            " 'Lglb', PERSON is Person, PERSON works_for ORGANIZATION"
        )
        self.assertEqual(query, expected)

    def test_simple_entity_link_and_attr_value_ilike(self):
        query = QE.get_queries(
            ["Person", "Organization"],
            ["Person#firstname", "Organization#name#lglb#I"],
        )
        expected = (
            "Any PERSON_FIRSTNAME, ORGANIZATION, PERSON WHERE PERSON firstname"
            " PERSON_FIRSTNAME, ORGANIZATION is Organization, ORGANIZATION name"
            " ILIKE 'lglb', PERSON is Person, PERSON works_for ORGANIZATION"
        )
        self.assertEqual(query, expected)

    def test_simple_entity_link_and_attr_value_ilike2(self):
        query = QE.get_queries(
            ["Person"],
            ["Person#firstname", "Organization#name#lglb#I"],
        )
        expected = (
            "Any PERSON_FIRSTNAME, ORGANIZATION, PERSON WHERE PERSON firstname"
            " PERSON_FIRSTNAME, ORGANIZATION is Organization, ORGANIZATION name"
            " ILIKE 'lglb', PERSON is Person, PERSON works_for ORGANIZATION"
        )
        self.assertEqual(query, expected)

    def test_multi_values(self):
        query = QE.get_queries(
            ["Project"],
            [
                "Organization#sector#énergie",
                "Component#type#centrale",
                "Component#version#1.2",
                "Project#name",
            ],
        )
        expected = (
            "Any ORGANIZATION, COMPONENT, PROJECT_NAME, PROJECT WHERE ORGANIZATION"
            " is Organization, ORGANIZATION sector 'énergie', COMPONENT is Component,"
            " COMPONENT type 'centrale', COMPONENT version '1.2', PROJECT name PROJECT_NAME,"
            " PROJECT is Project, PROJECT managed_by ORGANIZATION, PROJECT includes COMPONENT"
        )
        self.assertEqual(query, expected)
