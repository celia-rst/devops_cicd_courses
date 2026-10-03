describe("Formulaire de Connexion", () => {
  beforeEach(() => {
    cy.visit("/");
  });

  it("devrait activer le bouton uniquement lorsque le formulaire est valide", () => {
    // 1. État initial : le bouton doit être désactivé
    cy.get('[data-cy="login-submit-button"]').should("be.disabled");

    // 2. Email invalide (pas de @)
    cy.get('[data-cy="login-email-input"]').type("test");
    cy.get('[data-cy="login-password-input"]').type("password123");
    cy.get('[data-cy="login-submit-button"]').should("be.disabled");

    // 3. Mot de passe trop court (< 6 caractères)
    cy.get('[data-cy="login-email-input"]').clear().type("user@test.com");
    cy.get('[data-cy="login-password-input"]').clear().type("123");
    cy.get('[data-cy="login-submit-button"]').should("be.disabled");

    // 4. Formulaire totalement valide
    cy.get('[data-cy="login-password-input"]').clear().type("password123");
    cy.get('[data-cy="login-submit-button"]').should("be.enabled");
  });
});