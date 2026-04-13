/**
 * Vault404 TypeScript SDK
 *
 * The official SDK for interacting with Vault404 - the collective AI coding agent brain.
 * Every verified fix makes ALL AI agents smarter.
 *
 * @packageDocumentation
 *
 * @example
 * Basic Usage
 * ```typescript
 * import { Vault404Client } from 'vault404';
 *
 * const vault404 = new Vault404Client();
 *
 * // Find solutions for an error
 * const result = await vault404.findSolution({
 *   errorMessage: 'Cannot find module react',
 *   language: 'typescript'
 * });
 *
 * // Log an error fix
 * await vault404.logErrorFix({
 *   errorMessage: 'Module not found',
 *   solution: 'Run npm install'
 * });
 * ```
 *
 * @example
 * With Custom Configuration
 * ```typescript
 * import { Vault404Client } from 'vault404';
 *
 * const vault404 = new Vault404Client({
 *   apiUrl: 'http://localhost:8000',
 *   timeout: 60000,
 *   debug: true
 * });
 * ```
 *
 * @example
 * Error Handling
 * ```typescript
 * import { Vault404Client, NetworkError, ValidationError } from 'vault404';
 *
 * const vault404 = new Vault404Client();
 *
 * try {
 *   await vault404.findSolution({ errorMessage: '' });
 * } catch (error) {
 *   if (error instanceof ValidationError) {
 *     console.log('Invalid input:', error.field);
 *   } else if (error instanceof NetworkError) {
 *     console.log('Network issue:', error.message);
 *   }
 * }
 * ```
 */

// Main client
export { Vault404Client } from "./client.js";

// Error classes
export {
  Vault404Error,
  NetworkError,
  ApiError,
  TimeoutError,
  ValidationError,
  AuthenticationError,
  RateLimitError,
  NotFoundError,
} from "./errors.js";

// Types
export type {
  // Configuration
  Vault404ClientOptions,

  // Context
  Context,

  // Error Fix types
  ErrorInfo,
  SolutionInfo,
  LogErrorFixOptions,
  FindSolutionOptions,
  Solution,
  FindSolutionResult,

  // Decision types
  LogDecisionOptions,
  FindDecisionOptions,
  Decision,
  FindDecisionResult,

  // Pattern types
  LogPatternOptions,
  FindPatternOptions,
  Pattern,
  FindPatternResult,

  // Verification types
  VerifySolutionOptions,
  VerifySolutionResult,

  // Stats types
  Vault404Stats,
  StatsResult,

  // Generic result types
  LogResult,
} from "./types.js";

// Version
export const VERSION = "0.1.0";

// Default export for convenience
export { Vault404Client as default } from "./client.js";
