import { overrideSegment } from './VCS';

export function Warp(segment: string, override: string): void {
  overrideSegment(segment, override);
}
