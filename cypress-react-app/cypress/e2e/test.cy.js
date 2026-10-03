describe("Mon premier test", () => {
    it("Vérifie que la page d'accueil se charge", () => {
    cy.visit("/"); // Grâce à baseUrl, cela visitera http://localhost:5173
    cy.contains("Connexion").should("be.visible");
    });
});
   