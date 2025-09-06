    #pragma header

	layout (location = 0) out vec4 fragColor;

	in vec2 uv;
	uniform sampler2D u_texture_0;

	uniform float scroll;

	void main()
    {
		vec2 pos = uv;
		pos.x += scroll*(uv.y-0.5);
		fragColor = texture(u_texture_0, pos);
    }