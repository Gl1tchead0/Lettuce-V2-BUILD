    #version 330

	layout (location = 0) out vec4 fragColor;

	in vec2 uv;
	uniform sampler2D u_texture_0;

	uniform float scroll;

    void main()
    {
		vec2 pos = uv;
		pos.x -= 0.5;
		pos.x /= uv.y;
		pos.x += 0.5;
		fragColor = texture(u_texture_0, vec2(mod(pos.x+scroll,1.0),pos.y));
    }