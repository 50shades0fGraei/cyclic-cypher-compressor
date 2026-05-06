import { Jin } from '../Jin';
export function installCubixOS() {
    Jin.order("altar.summon");
    Jin.command("altar.summon", "build");
    Jin.command("altar.summon", "run");
    Jin.demand("vault.echo", "protect");
}
