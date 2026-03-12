describe('Atlas Telemetry Overlays', function() {
  it('should have agent telemetry toggle', function() {
    cy.visit('http://localhost:4173');
    cy.get('#toggle-agent-telemetry').should('exist');
  });

  it('should have navigation toggle', function() {
    cy.visit('http://localhost:4173');
    cy.get('#toggle-navigation').should('exist');
  });
});
