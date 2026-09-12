extends SceneTree

# 전투 계산식 콘솔 검증.
# 실행: godot --headless --path . --script tools/verify_battle_rules.gd

func _init() -> void:
	var errors := 0
	print("--- 상성 배율 (게임→테크→디자인→만화→게임) ---")
	var names := ["게임", "테크", "디자인", "만화"]
	for a in 4:
		var row := "  %-4s 공격: " % names[a]
		for d in 4:
			row += "%s=%.1f  " % [names[d], BattleRules.element_multiplier(a, d)]
		print(row)
	if BattleRules.element_multiplier(BattleRules.Element.GAME, BattleRules.Element.TECH) != 2.0: errors += 1
	if BattleRules.element_multiplier(BattleRules.Element.TECH, BattleRules.Element.GAME) != 1.0: errors += 1

	print("--- 데미지 (roll 고정 1.0) ---")
	var pix = load("res://data/idis/pixelmong.tres")
	var sol = load("res://data/idis/soldering.tres")
	var eb = load("res://data/moves/early_bird.tres")
	var mult = BattleRules.element_multiplier(pix.element, sol.element)
	var dmg = BattleRules.calculate_damage(pix.attack, sol.defense, eb.power, mult, 1.0)
	print("  픽셀몽(공%d) → 납땜이(방%d, HP%d) 얼리버드(위력%d) x%.1f = %d 데미지, %d턴 KO" % [
		pix.attack, sol.defense, sol.max_hp, eb.power, mult, dmg, ceili(float(sol.max_hp) / dmg)])
	if dmg <= 0: errors += 1
	print("  최소 데미지 보장: ", BattleRules.calculate_damage(1, 999, 1, 1.0, 0.85))

	print("--- 영입 성공률 ---")
	for hp in [42, 21, 1]:
		print("  HP %2d/42 → %.0f%%" % [hp, BattleRules.capture_chance(hp, 42) * 100.0])
	if absf(BattleRules.capture_chance(21, 42) - 0.5) > 0.001: errors += 1

	print("=== 결과: 에러 %d개 ===" % errors)
	quit(1 if errors > 0 else 0)
