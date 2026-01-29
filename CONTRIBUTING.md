# Contributing to JHRIS

Thank you for considering contributing to JHRIS! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Node version, browser)
- Screenshots if applicable

### Suggesting Features

Feature requests are welcome! Please:
- Search existing issues first
- Provide a clear use case
- Explain the expected behavior
- Consider the scope and complexity

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Write clean, documented code
   - Add tests if applicable

4. **Test your changes**
   ```bash
   # Backend tests
   cd backend
   npm test
   
   # Frontend testing
   # Test manually in browser
   ```

5. **Commit your changes**
   ```bash
   git commit -m "Add feature: description"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide a clear description
   - Reference any related issues
   - Wait for review

## Development Setup

### Prerequisites
- Node.js 14+
- npm or yarn
- Git

### Setup
```bash
git clone https://github.com/ninoyerbas/JHRIS.git
cd JHRIS
chmod +x start.sh
./start.sh
```

## Code Style

### JavaScript
- Use ES6+ features
- Use semicolons
- 2-space indentation
- Meaningful variable names
- Add comments for complex logic

### Example:
```javascript
// Good
async function fetchEmployeeData(employeeId) {
  try {
    const data = await apiRequest(`/employees/${employeeId}`);
    return data;
  } catch (error) {
    console.error('Error fetching employee:', error);
    throw error;
  }
}

// Avoid
async function getData(id) {
  return await apiRequest(`/employees/${id}`);
}
```

## Project Structure

```
JHRIS/
├── backend/           # Node.js/Express API
│   ├── src/
│   │   ├── config/    # Database and configuration
│   │   ├── controllers/ # Business logic
│   │   ├── middleware/  # Auth and other middleware
│   │   └── routes/      # API routes
│   └── package.json
├── frontend/          # Frontend application
│   └── public/
│       ├── css/       # Stylesheets
│       ├── js/        # JavaScript
│       └── index.html
└── docs/              # Documentation
```

## Testing

### Backend API Testing
```bash
# Test with curl
curl http://localhost:3001/api/health

# Or create tests with Jest/Mocha (future)
npm test
```

### Frontend Testing
- Test in multiple browsers (Chrome, Firefox, Safari)
- Test responsive design
- Test all user flows

## Security

### Reporting Security Issues
**Do not open public issues for security vulnerabilities.**

Email security concerns to the maintainers privately.

### Security Guidelines
- Never commit sensitive data (.env files, keys)
- Use parameterized queries (already implemented)
- Validate all inputs
- Follow OWASP guidelines
- Keep dependencies updated

## Database Changes

When modifying the database schema:

1. Update `backend/src/config/database.js`
2. Document changes in migration notes
3. Consider backward compatibility
4. Test with existing data

## API Changes

When modifying APIs:

1. Maintain backward compatibility when possible
2. Version new APIs if breaking changes
3. Update documentation
4. Update frontend accordingly

## Documentation

- Update README.md for user-facing changes
- Update docs/ for technical changes
- Add JSDoc comments for functions
- Update API documentation

## Pull Request Checklist

Before submitting a PR:

- [ ] Code follows the style guide
- [ ] All tests pass
- [ ] New code has tests (if applicable)
- [ ] Documentation is updated
- [ ] No sensitive data in commits
- [ ] Commit messages are clear
- [ ] PR description explains the changes

## Review Process

1. Maintainer reviews code
2. Feedback and discussions
3. Make requested changes
4. Approval and merge

## Getting Help

- Check existing documentation
- Search closed issues
- Ask in discussions
- Contact maintainers

## Code of Conduct

- Be respectful and professional
- Welcome newcomers
- Focus on constructive feedback
- Help others learn

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (ISC).

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes for significant contributions

Thank you for contributing to JHRIS! 🎉
