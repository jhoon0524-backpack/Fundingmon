extends SceneTree

# 헤드리스 검증: data/ 의 .tres 가 전부 로드되는지, 참조가 살아 있는지 확인한다.
# 실행: godot --headless --path . --script tools/verify_resources.gd

func _init() -> void:
	var errors := 0
	var idis := _list_tres("res://data/idis")
	var moves := _list_tres("res://data/moves")
	print("아이디 파일 %d개, 기술 파일 %d개" % [idis.size(), moves.size()])

	for p in moves:
		var r = load(p)
		if r == null:
			printerr("로드 실패: ", p); errors += 1; continue
		print("  [기술] %-28s %-10s 속성=%d 위력=%d" % [p.get_file(), r.display_name, r.element, r.power])

	for p in idis:
		var r = load(p)
		if r == null:
			printerr("로드 실패: ", p); errors += 1; continue
		var evo := "-"
		if r.evolves_into != null:
			evo = str(r.evolves_into.display_name)
		var move_count: int = r.moves.size() if "moves" in r else -1
		print("  [아이디] %-22s %-10s 속성=%d HP=%d 공=%d 방=%d 속=%d 기술=%d 진화→%s" % [
			p.get_file(), r.display_name, r.element, r.max_hp, r.attack, r.defense, r.speed, move_count, evo])

	# 메인 씬 로드
	var main_path: String = ProjectSettings.get_setting("application/run/main_scene")
	var scene = load(main_path)
	if scene == null:
		printerr("메인 씬 로드 실패: ", main_path); errors += 1
	else:
		var inst = scene.instantiate()
		print("메인 씬 OK: %s (루트=%s, 자식=%d)" % [main_path, inst.get_class(), inst.get_child_count()])
		inst.free()

	# 인풋 맵
	var actions := ["move_up", "move_down", "move_left", "move_right", "confirm", "cancel"]
	for a in actions:
		if not InputMap.has_action(a):
			printerr("인풋 액션 없음: ", a); errors += 1
	print("인풋 맵: %d/%d 존재" % [actions.filter(func(a): return InputMap.has_action(a)).size(), actions.size()])

	# 해상도 / 스트레치 / 필터
	print("해상도 %sx%s, 창 %sx%s, stretch=%s/%s, filter=%s, renderer=%s" % [
		ProjectSettings.get_setting("display/window/size/viewport_width"),
		ProjectSettings.get_setting("display/window/size/viewport_height"),
		ProjectSettings.get_setting("display/window/size/window_width_override"),
		ProjectSettings.get_setting("display/window/size/window_height_override"),
		ProjectSettings.get_setting("display/window/stretch/mode"),
		ProjectSettings.get_setting("display/window/stretch/aspect"),
		ProjectSettings.get_setting("rendering/textures/canvas_textures/default_texture_filter"),
		ProjectSettings.get_setting("rendering/renderer/rendering_method")])

	print("=== 결과: 에러 %d개 ===" % errors)
	quit(1 if errors > 0 else 0)

func _list_tres(dir_path: String) -> Array[String]:
	var out: Array[String] = []
	var d := DirAccess.open(dir_path)
	if d == null:
		printerr("폴더 없음: ", dir_path); return out
	for f in d.get_files():
		if f.ends_with(".tres"):
			out.append(dir_path + "/" + f)
	out.sort()
	return out
