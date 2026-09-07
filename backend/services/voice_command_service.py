"""
NIRMAAN - Voice Command & Conversational Assistant Service
Parses spoken commands to update catalog attributes, trigger pricing calculations, or perform marketplace actions.
"""
from typing import Dict, Any
from ..models.schemas import VoiceCommandRequest, VoiceCommandResponse

class VoiceCommandService:
    @staticmethod
    def process_command(request: VoiceCommandRequest) -> VoiceCommandResponse:
        cmd = request.command_text.lower().strip()
        updated_fields = {}
        action = "general"
        message = "Command understood."

        # 1. Attribute Modification Commands
        if "color" in cmd or "रंग" in cmd:
            if "blue" in cmd or "नीला" in cmd:
                updated_fields["color"] = "Indigo Blue"
                message = "Updated product color to Indigo Blue."
            elif "red" in cmd or "लाल" in cmd:
                updated_fields["color"] = "Terracotta Red"
                message = "Updated product color to Terracotta Red."
            elif "gold" in cmd or "सुनहरा" in cmd or "पीला" in cmd:
                updated_fields["color"] = "Antique Gold"
                message = "Updated product color to Antique Gold."
            else:
                updated_fields["color"] = cmd.replace("change color to", "").replace("रंग बदलो", "").strip().title()
                message = f"Updated color to {updated_fields['color']}."
            action = "update_attribute"

        elif "material" in cmd or "सामग्री" in cmd or "मिट्टी" in cmd or "पीतल" in cmd:
            if "clay" in cmd or "मिट्टी" in cmd:
                updated_fields["material"] = "Natural Terracotta Clay"
            elif "brass" in cmd or "पीतल" in cmd:
                updated_fields["material"] = "Pure Solid Brass"
            elif "bamboo" in cmd or "बांस" in cmd:
                updated_fields["material"] = "Seasoned Bamboo Cane"
            else:
                updated_fields["material"] = cmd.replace("change material to", "").strip().title()
            message = f"Updated material to {updated_fields['material']}."
            action = "update_attribute"

        # 2. Publication Commands
        elif any(w in cmd for w in ["publish", "प्रकाशित", "live", "बेचो", "दुकान पर डालो"]):
            action = "publish_product"
            message = "Publishing your handcrafted product to the NIRMAAN marketplace feed."

        # 3. Pricing & Market Commands
        elif any(w in cmd for w in ["charge", "price", "कीमत", "दाम", "लागत", "cost"]):
            action = "calculate_price"
            message = "Opening Pricing Intelligence to evaluate your production cost and market range."

        elif any(w in cmd for w in ["market", "बाजार", "similar", "दुकान", "compare"]):
            action = "show_market"
            message = "Checking current market prices and comparable handcrafted listings across India."

        # 4. Catalog & Collection Commands
        elif any(w in cmd for w in ["catalog", "संग्रह", "collection", "diwali"]):
            action = "add_to_catalog"
            message = "Ready to add this product to your digital collection."

        # 5. Help & Support Commands
        elif any(w in cmd for w in ["help", "मदद", "सहायता", "guide", "कस्टमर केयर"]):
            action = "help"
            message = "NIRMAAN voice assistant is here to help you turn photos and voice into catalogs and sales."

        # 6. Description Additions
        elif any(w in cmd for w in ["add", "जोड़ो", "जोड़िए"]):
            if "handmade" in cmd or "हाथ से" in cmd:
                updated_fields["craft_type"] = "100% Handcrafted Artisan Work"
                message = "Added handmade craft highlight to catalog."
                action = "update_attribute"

        return VoiceCommandResponse(
            action=action,
            message=message,
            updated_fields=updated_fields
        )

voice_command_service = VoiceCommandService()
