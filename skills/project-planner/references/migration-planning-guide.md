# Migration Planning Guide

Use this guide when planning framework or library version migrations for Python/React full-stack projects. Migrations require their own planning discipline — they touch many files, introduce deprecation risks, and need careful phasing.

## Migration Planning Workflow

### 1. Inventory Current State

Before planning any migration:
- Current version of the library/framework
- List of deprecated APIs currently used (search with `Grep`)
- Third-party dependencies that depend on the library
- Test coverage for affected areas

### 2. Research Target Version

For the version you're migrating to:
- Read official migration guide and changelog
- Identify breaking changes
- Check for available codemods (automated migration scripts)
- Verify third-party library compatibility
- Note new features that become available after migration

### 3. Create Compatibility Matrix

| Dependency | Current Version | Compatible with Target? | Action Needed |
|-----------|----------------|------------------------|---------------|
| [lib 1]   | x.y.z          | Yes / No / Unknown     | [upgrade/replace/none] |
| [lib 2]   | x.y.z          | Yes / No / Unknown     | [upgrade/replace/none] |

### 4. Plan Migration Phases

Migrations should be phased to minimize risk:

**Phase 1: Preparation (no version change)**
- Remove deprecated API usage that has modern alternatives
- Add compatibility shims where needed
- Increase test coverage for migration-affected areas

**Phase 2: Version Bump**
- Update the dependency version
- Run codemods
- Fix compilation/build errors
- Run test suite

**Phase 3: Adopt New Features**
- Gradually adopt new APIs and patterns
- Remove compatibility shims
- Update documentation

**Phase 4: Cleanup**
- Remove old code paths
- Update remaining deprecated patterns
- Final test pass

### 5. Define Rollback Plan

Every migration must have a rollback strategy:
- Git revert to pre-migration commit
- Dependency lock file preserved (package-lock.json, poetry.lock)
- Database migrations must be reversible if applicable
- Feature flags to disable new code paths if needed

---

## Common Migration Patterns

### React 18 → React 19

**Deprecated APIs to remove:**
- `forwardRef` → pass `ref` as a regular prop
- `<Context.Provider>` → use `<Context>` directly
- Class components → function components with hooks
- `ReactDOM.render()` → `createRoot()`
- `useFormState` → `useActionState`

**New features to adopt:**
- React Compiler (replaces manual `useMemo`/`useCallback`/`memo`)
- Server Components (for data-fetching, static content)
- Actions API (form handling, async operations)
- `use()` hook (promise resolution in components)

**Codemod:** `npx @react-codemod/react-19`

**Planning order:**
1. Audit deprecated API usage (`grep -r "forwardRef\|Context\.Provider\|ReactDOM\.render" src/`)
2. Upgrade dependencies
3. Run codemod
4. Manual fixes for codemod gaps
5. Enable React Compiler (optional, per-component)
6. Identify Server Component candidates
7. Full test suite

### FastAPI + Pydantic v1 → v2

**Key changes:**
- `validator` → `field_validator`
- `root_validator` → `model_validator`
- `schema_extra` → `model_config` with `json_schema_extra`
- `orm_mode = True` → `from_attributes = True`
- `.dict()` → `.model_dump()`
- `.json()` → `.model_dump_json()`

**Planning order:**
1. Audit Pydantic v1 usage in schemas
2. Update FastAPI to version with Pydantic v2 support
3. Update schema files (can be done file-by-file)
4. Update all `.dict()` and `.json()` calls
5. Test each endpoint

### SQLAlchemy 1.4 → 2.0+

**Key changes:**
- `Column()` → `mapped_column()` with `Mapped[]` type annotations
- `relationship()` gets type annotations
- Session API changes (2.0-style execution)
- `Query` API deprecated → use `select()` statements

**Planning order:**
1. Enable SQLAlchemy 2.0 deprecation warnings
2. Migrate models to `Mapped`/`mapped_column` style
3. Replace `Query` API with `select()` statements
4. Update session management to 2.0 patterns
5. Test all database operations

### TypeScript 5.x → 7.x

**Key changes:**
- Strict mode becomes default
- ES5 target dropped
- AMD/UMD/SystemJS removed
- Classic Node module resolution removed
- Go-based compiler (~10x faster)

**Planning order:**
1. Enable `"strict": true` in tsconfig.json now
2. Fix all strict mode errors
3. Remove ES5/AMD/UMD targets if used
4. Switch to modern module resolution
5. Upgrade TypeScript version
6. Verify build with new compiler

---

## Risk Assessment for Migrations

| Risk Category | Typical Impact | Mitigation |
|--------------|---------------|------------|
| Breaking API changes | Build failures | Run codemods, fix incrementally |
| Third-party incompatibility | Runtime errors | Check compatibility before upgrading |
| Subtle behavior changes | Test failures | High test coverage before migration |
| Performance regression | Slower app | Benchmark before and after |
| Rollback complexity | Delayed rollback | Keep rollback plan ready, use feature flags |

---

## Migration Checklist

- [ ] Current version documented
- [ ] Target version changelog reviewed
- [ ] Breaking changes identified
- [ ] Third-party compatibility verified
- [ ] Codemods identified and tested
- [ ] Test coverage adequate for affected areas
- [ ] Migration phases defined
- [ ] Rollback plan documented
- [ ] Team informed of migration timeline
- [ ] Staging environment tested
- [ ] Performance benchmarks compared
