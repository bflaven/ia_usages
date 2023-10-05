
# Convert the following code from Gherkin syntax to Cypress code, please generate real code for cut and paste :

Given I click on the "//[@id='content--create']" element
And I fill the "wire_title" field with "{{startDateString}} Test Wire title CodeceptJS {{RandomString}} "
And I click on the "//[@id='wire_save']" element
And I wait for 20 seconds
And I refresh the page
And I say "--- {{TOTEM_TEST_MAN}}"
And I say "--- Content saved"
When IMAGES_DIRECTORY_STATUS is "empty"
Then I say "--- IMAGES_DIRECTORY_STATUS is EMPTY"
When IMAGES_DIRECTORY_STATUS is "old"
Then I say "--- IMAGES_DIRECTORY_STATUS is OLD"
And I call the "BachAddWireImage" function
When IMAGES_DIRECTORY_STATUS is "OK"
Then I say "--- IMAGES_DIRECTORY_STATUS is OK"
And I call the "BachAddWireImage" function
And I click on the "//[@id='wire_save']" element
And I wait for 10 seconds
And I say "--- No test for URL"
And I select the "radio-PUBLISHED" option
And I wait for the element "//[@id='wire_save']" for 20 seconds
And I click on the "//[@id='wire_save']" element
And I wait for 10 seconds
And I wait for the element "//[@id='radio-PUBLISHED']" for 20 seconds