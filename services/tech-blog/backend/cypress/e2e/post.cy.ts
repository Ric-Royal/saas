describe('Post Management', () => {
  beforeEach(() => {
    // Reset database before each test
    cy.request('POST', 'http://localhost:4000/api/test/reset');
    cy.visit('/posts');
  });

  it('should create a new post', () => {
    cy.get('[data-cy=new-post-button]').click();
    cy.get('[data-cy=post-title]').type('Test Post');
    cy.get('[data-cy=post-content]').type('This is a test post content');
    cy.get('[data-cy=post-tags]').type('test,e2e{enter}');
    cy.get('[data-cy=submit-post]').click();

    // Verify post appears in the list
    cy.get('[data-cy=post-list]')
      .should('contain', 'Test Post')
      .and('contain', 'This is a test post content');
  });

  it('should update an existing post', () => {
    // Create a post first
    cy.request('POST', 'http://localhost:4000/api/posts', {
      title: 'Original Post',
      content: 'Original content',
      tags: ['original']
    });

    cy.visit('/posts');
    cy.get('[data-cy=edit-post-button]').first().click();
    cy.get('[data-cy=post-title]').clear().type('Updated Post');
    cy.get('[data-cy=submit-post]').click();

    // Verify update
    cy.get('[data-cy=post-list]')
      .should('contain', 'Updated Post')
      .and('not.contain', 'Original Post');
  });

  it('should delete a post', () => {
    // Create a post first
    cy.request('POST', 'http://localhost:4000/api/posts', {
      title: 'Post to Delete',
      content: 'This post will be deleted',
      tags: ['delete']
    });

    cy.visit('/posts');
    cy.get('[data-cy=delete-post-button]').first().click();
    cy.get('[data-cy=confirm-delete]').click();

    // Verify deletion
    cy.get('[data-cy=post-list]')
      .should('not.contain', 'Post to Delete');
  });

  it('should show real-time updates', () => {
    // Open two browser windows
    cy.visit('/posts');
    cy.window().then((win) => {
      const newWindow = win.open('/posts');
      
      // Create post in first window
      cy.get('[data-cy=new-post-button]').click();
      cy.get('[data-cy=post-title]').type('Real-time Test Post');
      cy.get('[data-cy=submit-post]').click();

      // Verify post appears in second window
      cy.wrap(newWindow).within(() => {
        cy.get('[data-cy=post-list]')
          .should('contain', 'Real-time Test Post');
      });
    });
  });
}); 