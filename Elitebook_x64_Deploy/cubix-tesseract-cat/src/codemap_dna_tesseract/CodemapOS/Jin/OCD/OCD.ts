import { stageSegment } from './VCS';

export function OCD(segment: string, state: boolean): void {
  stageSegment(segment, state);
}
