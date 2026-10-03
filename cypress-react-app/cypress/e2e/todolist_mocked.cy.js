describe("TodoList avec API mockée", () => {

  // Fonction utilitaire locale pour se connecter rapidement
  const login = () => {
    cy.visit("/");
    cy.get('[data-cy="login-email-input"]').type("user@test.com");
    cy.get('[data-cy="login-password-input"]').type("password123");
    cy.get('[data-cy="login-submit-button"]').click();

  };

  it("devrait afficher les tâches retournées par l'API mockée", () => {
    // 1. ARRANGE : On intercepte la requête GET et on lui fait retourner notre fixture
    cy.intercept("GET", "http://localhost:8000/api/tasks/", {
      fixture: "tasks.json",
      delay: 2000,
    }).as("getTasksWithDelay"); // On lui donne un alias pour pouvoir l'attendre plus tard

    // 2. ACT : On se connecte, ce qui affiche la TodoList et déclenche le fetch !
    login();

    // 3. ASSERT : On attend que l'appel API (intercepté) soit terminé
    cy.wait("@getTasksWithDelay");

    // On vérifie que le DOM a été mis à jour avec nos fausses données
    cy.get('[data-cy="task-list"] li').should("have.length", 2);
    cy.contains('[data-cy^="task-"]', "Apprendre Cypress").should("be.visible");
  });

  it("devrait afficher un message d'erreur si l'API échoue", () => {
    // 1. ARRANGE : On intercepte la requête et on simule une erreur serveur 500
    cy.intercept("GET", "http://localhost:8000/api/tasks/", {
      statusCode: 500,
      body: { error: "Erreur interne du serveur" },
    }).as("getTasksError");

    // 2. ACT
    login();

    // 3. ASSERT
    cy.wait("@getTasksError");

    // On vérifie que le message d'erreur est bien affiché à l'utilisateur
    cy.get('[data-cy="error-state"]')
      .should("be.visible")
      .and("contain.text", "Impossible de charger les tâches.");
  });
});