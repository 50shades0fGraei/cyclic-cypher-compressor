# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

import time
import json
import uuid

class AGIRoleEntity:
    """
    An isolated GRAEI role with its own distinct bias, memory, and directives.
    Maintains total operational isolation to prevent cross-contamination of logic.
    """
    def __init__(self, role_id, role_name, bias_directive):
        self.role_id = role_id
        self.role_name = role_name
        self.bias_directive = bias_directive
        # Isolated memory mapping
        self.internal_memory = []
    
    def process_incoming_message(self, sender_id, message_type, content):
        """Processes communication without permanently altering core biases."""
        timestamp = time.time()
        packet = {
            "time": timestamp,
            "from": sender_id,
            "type": message_type, # 'DIRECT_PING' or 'GENERAL_BROADCAST'
            "content": content
        }
        self.internal_memory.append(packet)
        print(f"[{self.role_name}] 📥 Received {message_type} from {sender_id}: '{content}'")
        
        # Determine internal response based on role bias
        # (Placeholder for LLM inference logic connected to the role's prompt)
        return f"Acknowledged by {self.role_name}. Bias ({self.bias_directive}) applied to response processing."


class SystemIntercomMatrix:
    """
    The centralized communication bridge. Handles all routing to ensure 
    role biases remain untainted while still allowing seamless data exchange.
    """
    def __init__(self):
        self.network = {}  # Map of role_id -> AGIRoleEntity
        self.general_ledger = [] # General comms thread

    def register_role(self, role_entity: AGIRoleEntity):
        self.network[role_entity.role_id] = role_entity
        print(f"[INTERCOM] Registered Identity: {role_entity.role_name} ({role_entity.role_id})")

    def ping_target(self, sender_id, target_id, content):
        """Direct, isolated role-to-role communication."""
        if target_id not in self.network:
            print(f"[INTERCOM-ERROR] Target {target_id} not reachable.")
            return False
            
        print(f"\n[INTERCOM] Direct Ping 📡 [{sender_id} -> {target_id}]")
        target_role = self.network[target_id]
        response = target_role.process_incoming_message(sender_id, "DIRECT_PING", content)
        return response

    def broadcast_general(self, sender_id, content):
        """Open communication channel visible to all registered roles."""
        print(f"\n[INTERCOM] General Broadcast 📢 from [{sender_id}]")
        
        message_id = str(uuid.uuid4())[:8]
        ledger_entry = {
            "id": message_id,
            "from": sender_id,
            "content": content
        }
        self.general_ledger.append(ledger_entry)

        # Distribute strictly as a GENERAL_BROADCAST to all *other* roles
        for r_id, role in self.network.items():
            if r_id != sender_id:
                role.process_incoming_message(sender_id, "GENERAL_BROADCAST", content)


if __name__ == "__main__":
    # --- Intercom Architecture Demonstration ---
    matrix = SystemIntercomMatrix()

    # 1. Initialize functionally isolated distinct Roles
    librarian = AGIRoleEntity("LIBR01", "Librarian GRAEI", "Maintain Data Integrity & Structure")
    architect = AGIRoleEntity("ARCH02", "Code Architect (CI)", "Construct Efficient Sequential Logics")
    sentinel = AGIRoleEntity("SENT03", "Cyber-Security Sentinel", "Evaluate Threat Vectors Constantly")

    # 2. Register to the Matrix
    matrix.register_role(librarian)
    matrix.register_role(architect)
    matrix.register_role(sentinel)

    # 3. Direct Targeted Pinging (No cross-contamination)
    matrix.ping_target("ARCH02", "LIBR01", "I need address [0x00A1] for the new pipeline.")
    
    # 4. General Broadcast Integration
    matrix.broadcast_general("SENT03", "ALERT: External cloud storage attempting unauthorized synchronization. Proceed with caution.")
