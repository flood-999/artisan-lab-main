/**
 * NIRMAAN - Pricing Studio Engine
 * Manages deterministic Cost Calculator, Market Intelligence, and 5-tier Pricing Insights.
 */
import { ApiClient } from "./api.js";

export const PricingManager = {
  currentCalculation: null,
  currentMarketCheck: null,
  currentInsight: null,

  async runCalculation(inputs) {
    const defaultInputs = {
      material_cost: parseFloat(inputs.materialCost) || 200,
      time_spent_hours: parseFloat(inputs.timeHours) || 4,
      labour_rate_hourly: parseFloat(inputs.labourRate) || 150,
      wastage_percent: parseFloat(inputs.wastagePercent) || 0,
      packaging_cost: parseFloat(inputs.packagingCost) || 0,
      other_costs: parseFloat(inputs.otherCosts) || 0,
      selling_costs: parseFloat(inputs.sellingCosts) || 0,
      profit_margin_percent: parseFloat(inputs.profitMargin) || 30,
      premium_multiplier: parseFloat(inputs.premiumMultiplier) || 1.20
    };

    try {
      this.currentCalculation = await ApiClient.calculateCostPrice(defaultInputs);
      return this.currentCalculation;
    } catch (e) {
      // Local deterministic offline math fallback
      const wastage = defaultInputs.material_cost * (defaultInputs.wastage_percent / 100);
      const labour = defaultInputs.time_spent_hours * defaultInputs.labour_rate_hourly;
      const totalCost = defaultInputs.material_cost + wastage + labour + defaultInputs.packaging_cost + defaultInputs.other_costs + defaultInputs.selling_costs;
      const profit = totalCost * (defaultInputs.profit_margin_percent / 100);
      const recPrice = totalCost + profit;
      const premPrice = recPrice * defaultInputs.premium_multiplier;

      this.currentCalculation = {
        material_cost: defaultInputs.material_cost,
        wastage_cost: wastage,
        labour_cost: labour,
        packaging_cost: defaultInputs.packaging_cost,
        other_costs: defaultInputs.other_costs,
        selling_costs: defaultInputs.selling_costs,
        total_cost: totalCost,
        cost_floor: totalCost,
        recommended_price: Math.round(recPrice),
        estimated_profit: Math.round(profit),
        premium_price: Math.round(premPrice),
        currency: "INR",
        breakdown_text: `Material: ₹${defaultInputs.material_cost} | Labour: ₹${labour} | Total: ₹${totalCost}`
      };
      return this.currentCalculation;
    }
  },

  async runMarketCheck(productName, category, material, craftType, isHandmade = true) {
    try {
      this.currentMarketCheck = await ApiClient.checkMarketPrice({
        product_name: productName || "Handmade Craft",
        category: category || "Handicrafts",
        material: material || "Natural Material",
        craft_type: craftType || "Handmade",
        is_handmade: isHandmade
      });
      return this.currentMarketCheck;
    } catch (e) {
      console.warn("Market check fallback:", e);
      return null;
    }
  },

  async runPricingInsight(currentPrice) {
    try {
      this.currentInsight = await ApiClient.getPricingInsight({
        current_price: currentPrice ? parseFloat(currentPrice) : (this.currentCalculation?.recommended_price || 500),
        calculation: this.currentCalculation,
        market_check: this.currentMarketCheck
      });
      return this.currentInsight;
    } catch (e) {
      console.warn("Insight error:", e);
      return null;
    }
  }
};
