extends SceneTree

# QA 3 (시각 QA) 용 스크린샷. 메인 씬을 띄우고 오른쪽으로 잠깐 걷게 한 뒤 캡처한다.
# 헤드리스가 아닌 일반 실행 파일로 돌려야 화면이 렌더링된다.
# 실행: godot --path . --script tools/qa_screenshot.gd -- <저장할 png 절대경로>

var frames := 0
var out_path := "qa_screenshot.png"
var player: Node2D
var start_pos := Vector2.ZERO


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() > 0:
		out_path = args[0]
	var scene: PackedScene = load(ProjectSettings.get_setting("application/run/main_scene"))
	root.add_child(scene.instantiate())
	player = root.get_node_or_null("Main/Player")
	process_frame.connect(_on_frame)


func _on_frame() -> void:
	frames += 1
	if frames == 5 and player:
		start_pos = player.position
		Input.action_press("move_right")
	if frames == 35 and player:
		Input.action_release("move_right")
		var moved := player.position - start_pos
		print("플레이어 이동: %s → %s (30프레임 동안 %.1fpx, 방향=%s, 애니=%s)" % [
			start_pos, player.position, moved.length(), player.facing, player.sprite.animation])
	if frames == 40:
		var img := root.get_texture().get_image()
		var err := img.save_png(out_path)
		print("스크린샷 저장 %s (%dx%d) err=%d" % [out_path, img.get_width(), img.get_height(), err])
		quit()
