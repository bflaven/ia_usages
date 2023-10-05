# generate_code_ia_gehrkin.feature
# source for GPT query
# Write a test in Gherkin syntax to test a website main navigation

Feature: Main Navigation
  As a user
  I want to be able to navigate the website using the main navigation menu
  So that I can access the different sections of the website easily

Scenario: Navigation links
  Given I am on the website homepage
  When I click on the "About" link in the main navigation
  Then I should be taken to the "About" page

Scenario: Sub-Navigation links
  Given I am on the website homepage
  When I click on the "Services" link in the main navigation
  And I click on the "Consulting" sub-navigation link
  Then I should be taken to the "Consulting" page

Scenario: Dropdown Navigation links
  Given I am on the website homepage
  When I hover over the "Products" link in the main navigation
  And I click on the "Software" dropdown link
  Then I should be taken to the "Software" page
