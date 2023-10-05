// GPT result :: Gherkin syntax to Cypress syntax

describe('Creating a Wire', () => {
  it('Create a Wire and set the status', () => {
    cy.get('#content--create').click()
    cy.get('#wire_title').type(`${Cypress.moment().format('YYYY-MM-DD')} Test Wire title CodeceptJS ${Math.random().toString(36).substring(7)}`)
    cy.get('#wire_save').click()
    cy.wait(20000)
    cy.reload()
    cy.log('--- TOTEM_TEST_MAN')
    cy.log('--- Content saved')

    if (Cypress.env('IMAGES_DIRECTORY_STATUS') === 'empty') {
      cy.log('--- IMAGES_DIRECTORY_STATUS is EMPTY')
    } else if (Cypress.env('IMAGES_DIRECTORY_STATUS') === 'old') {
      cy.log('--- IMAGES_DIRECTORY_STATUS is OLD')
      cy.call('BachAddWireImage')
    } else if (Cypress.env('IMAGES_DIRECTORY_STATUS') === 'OK') {
      cy.log('--- IMAGES_DIRECTORY_STATUS is OK')
      cy.call('BachAddWireImage')
      cy.get('#wire_save').click()
      cy.wait(10000)
    }

    cy.log('--- No test for URL')
    cy.get('[id="radio-PUBLISHED"]').click()
    cy.wait(20000)
    cy.get('#wire_save').click()
    cy.wait(10000)
    cy.get('#radio-PUBLISHED').should('be.visible').should('be.checked')
  })
})
