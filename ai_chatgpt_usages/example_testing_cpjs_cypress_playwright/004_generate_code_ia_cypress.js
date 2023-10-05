// 004_generate_code_ia_cypress.js
// source for GPT query
// Generate a login test with Cypress testing Framework:

describe('Login Test', function() {
  it('Visits the login page and attempts to log in', function() {
    cy.visit('https://your-website.com/login');

    cy.get('input[name="email"]')
      .type('test@email.com');

    cy.get('input[name="password"]')
      .type('password');

    cy.get('button[type="submit"]')
      .click();

    cy.contains('Welcome back, Test User!');
  });
});
