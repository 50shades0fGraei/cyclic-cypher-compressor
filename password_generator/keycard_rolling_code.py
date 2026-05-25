# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

import hashlib
import time

# Representing the cyclic alphabet
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "

class CypherDoorReader:
    def __init__(self, master_system_secret: str):
        # The reader knows the master secret but NEVER exposes it.
        self.secret = master_system_secret
        # The sync counter ensures the reader knows where the cycle is.
        self.expected_counter = 1
        
    def verify_swipe(self, numeric_code_read_from_card: str) -> bool:
        """
        The door reader calculates what the next numeric code *should* be,
        and compares it to what the keycard just transmitted.
        """
        # Calculate expected code based on current cyclic position
        expected = self._calculate_numeric_cypher(self.secret, self.expected_counter)
        
        if numeric_code_read_from_card == expected:
            # Shift the cycle forward so this code can NEVER be used again
            self.expected_counter += 1
            return True
            
        # Optional: Implement "Look-ahead" window here in case a button was pressed 
        # in someone's pocket and the card is slightly out of sync.
        return False
        
    def _calculate_numeric_cypher(self, secret: str, position: int) -> str:
        """
        Core math: Turns the secret and the cycle position into pure numbers.
        """
        seed = f"{secret}::CYCLE_{position}"
        h = hashlib.sha256(seed.encode()).digest()
        
        # Turn the hash into a pure 10-digit numeric sequence for the keycard
        # using modulo math on our 97-character concept logic.
        numeric_output = str(int.from_bytes(h[:8], 'big'))[:10]
        return numeric_output


class CypherSmartCard:
    def __init__(self, master_system_secret: str, starting_cycle: int = 1):
        # The physical card holds the secret and its current cycle position
        self.secret = master_system_secret
        self.cycle_position = starting_cycle
        
    def generate_swipe_data(self) -> str:
        """
        When touched to a reader, the card calculates the current cypher state
        and sends only a numeric code. It then rolls its cycle forward.
        """
        seed = f"{self.secret}::CYCLE_{self.cycle_position}"
        h = hashlib.sha256(seed.encode()).digest()
        
        numeric_output = str(int.from_bytes(h[:8], 'big'))[:10]
        
        # Advance the physical card's cycle
        self.cycle_position += 1
        
        return numeric_output

if __name__ == "__main__":
    print("=" * 60)
    print(" CYCLIC CYPHER ROLLING KEYCARD DEMONSTRATION ")
    print("=" * 60)
    
    # 1. Setup the system
    base_password = "MyHighlySecureCorporatePassword123"
    door_reader = CypherDoorReader(base_password)
    employee_badge = CypherSmartCard(base_password)
    
    print("\n[SYSTEM] Door Reader installed. Employee Badge issued.")
    print(f"[SYSTEM] The base password is secretly: '{base_password}'")
    print("[SYSTEM] No reader will ever transmit or display this password.\n")
    
    # 2. Simulate Swipes
    for i in range(1, 4):
        print("-" * 40)
        print(f"--- SWIPE EVENT {i} ---")
        
        # Threat model: Attacker is scanning the RFID signal!
        transmitted_code = employee_badge.generate_swipe_data()
        print(f"Badge physically transmits numeric code : {transmitted_code}")
        
        # At this exact moment, an attacker clones the code:
        cloned_hacker_code = transmitted_code
        
        # Door checks it
        success = door_reader.verify_swipe(transmitted_code)
        if success:
            print("[DOOR] Access Granted. Cycle advancing to next lock state.")
        
        # Hacker tries to use the cloned code right after
        print("\n[HACKER ALERT] Attacker tries to replay the stolen card code!")
        hacker_success = door_reader.verify_swipe(cloned_hacker_code)
        if not hacker_success:
            print("[DOOR] ALARM! ACCESS DENIED! That position in the cycle is dead.")
            
        time.sleep(1)
        
    print("\n" + "=" * 60)
