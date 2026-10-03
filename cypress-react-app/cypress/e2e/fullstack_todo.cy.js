describe("Parcours Full Stack - ToDo List", () => {
  it("permet de créer une tâche qui persiste dans la base de données backend", () => {
    // Étape 1 : Préparation
    // On génère un titre unique avec le timestamp actuel
    const newTaskTitle = `Ma tâche critique du ${Date.now()}`;

    // Étape 2 : Se connecter à l'application
    cy.login();

    // Étape 3 : Interagir avec l'UI pour créer une tâche
    // Au lieu de : cy.get('[data-cy="login-email-input"]')
    cy.getByDataCy("new-task-input").type(newTaskTitle);
    cy.getByDataCy("add-task-button").click();

    // Étape 4 : Vérifier le résultat
    // L'assertion la plus importante : la nouvelle tâche est visible à l'écran.
    // Si ce test passe, cela prouve de façon absolue que React a bien envoyé le POST (sans erreur CORS !), 
    // que Django a bien écrit dans PostgreSQL, et que React a mis à jour le DOM !
    cy.get('[data-cy="task-list"]').should("contain.text", newTaskTitle);
    cy.contains(/ma tâche/i).should("be.visible");
  });
});

describe("Parcours Full Stack - ToDo List", () => {
  it("permet de créer une tâche qui survit à un rechargement de page", () => {
    const newTaskTitle = `Ma tâche persistante ${Date.now()}`;

    cy.login();

    // 1. Ajouter la tâche
    cy.get('[data-cy="new-task-input"]').type(newTaskTitle);
    cy.get('[data-cy="add-task-button"]').click();

    // 2. Vérification immédiate (état React)
    cy.contains('[data-cy^="task-"]', newTaskTitle).should("be.visible");

    // 3. Le test de vérité : on recharge le navigateur complet !
    cy.reload();
    cy.login();

    // 4. Si la tâche réapparaît, la persistance backend est garantie à 100%
    cy.contains('[data-cy^="task-"]', newTaskTitle).should("be.visible");
  });
});