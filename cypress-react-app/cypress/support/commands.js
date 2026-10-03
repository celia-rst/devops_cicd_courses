// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })

// Crée une commande raccourcie pour cibler les attributs data-cy
Cypress.Commands.add("getByDataCy", (selector) => {
  return cy.get(`[data-cy="${selector}"]`);
});

// On ajoute la nouvelle commande globale
Cypress.Commands.add("login", () => {
  cy.visit("/");
  cy.get('[data-cy="login-email-input"]').type("user@test.com");
  cy.get('[data-cy="login-password-input"]').type("password123");
  cy.get('[data-cy="login-submit-button"]').click();
});