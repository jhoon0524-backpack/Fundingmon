class_name Player
extends CharacterBody2D

## 필드 플레이어. 4방향 이동과 방향별 걷기 애니메이션.
## 원점은 발밑이다. 타일 격자에 발을 맞추기 위해서다 (ART_SPEC.md 1장).

## GAME_SPEC.md 4장: 이동속도 120px/s
const SPEED := 120.0

@onready var sprite: AnimatedSprite2D = $AnimatedSprite2D

## 마지막으로 바라본 방향. 멈춰 있을 때 이 방향의 첫 프레임을 보여 준다.
var facing := "down"


func _physics_process(_delta: float) -> void:
	var input := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	# 4방향 이동: 대각선 입력이면 더 큰 축만 남긴다
	if absf(input.x) >= absf(input.y):
		input.y = 0.0
	else:
		input.x = 0.0

	velocity = input.normalized() * SPEED if input != Vector2.ZERO else Vector2.ZERO
	move_and_slide()
	_update_sprite(input)


func _update_sprite(input: Vector2) -> void:
	if input == Vector2.ZERO:
		if sprite.is_playing():
			sprite.stop()
			sprite.frame = 0
		return

	if input.x > 0.0:
		facing = "right"
	elif input.x < 0.0:
		facing = "left"
	elif input.y > 0.0:
		facing = "down"
	else:
		facing = "up"

	var anim := "walk_" + facing
	if sprite.animation != anim or not sprite.is_playing():
		sprite.play(anim)
