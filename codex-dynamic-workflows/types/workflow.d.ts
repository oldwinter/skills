/**
 * Conceptual workflow globals mirrored from pi-dynamic-workflows.
 *
 * Codex does not automatically expose these as runtime globals. This file is
 * documentation and editor help for teams that draft portable workflow plans.
 */

export interface WorkflowMeta {
  name: string;
  description: string;
  whenToUse?: string;
  phases?: Array<{ title: string; detail?: string; model?: string }>;
}

export interface AgentOptions<T = unknown> {
  label?: string;
  phase?: string;
  schema?: T;
  agentType?: string;
}

export declare const args: unknown;
export declare const cwd: string;
export declare const budget: {
  total: number | null;
  spent(): number;
  remaining(): number;
};

export declare function phase(title: string): void;
export declare function log(message: string): void;
export declare function agent<T = string>(prompt: string, opts?: AgentOptions): Promise<T>;
export declare function parallel<T>(thunks: Array<() => Promise<T>>): Promise<T[]>;
export declare function pipeline<T, U>(
  items: T[],
  ...stages: Array<(previous: unknown, original: T, index: number) => Promise<U> | U>
): Promise<U[]>;
