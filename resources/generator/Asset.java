package ua.iladrien.buildinggenerator.generator.assets;

import net.minecraft.block.BlockState;
import net.minecraft.block.Blocks;
import net.minecraft.state.properties.BlockStateProperties;
import ua.iladrien.buildinggenerator.generator.Asset;
import ua.iladrien.buildinggenerator.generator.Assets;
import ua.iladrien.buildinggenerator.generator.TileRotation;


public class {{class_name}} extends Asset {

    {{static_blocks}}

	@Override
	public void init() {
	    this.rotation = TileRotation.ROTATION_{{angle}};
		this.allowedInAir = {{allowedInAir}};
		this.allowedOnGround = {{allowedOnGround}};

        this.allowedOnNorthEdge = {{allowedOnNorthEdge}};
        this.allowedOnWestEdge = {{allowedOnWestEdge}};
        this.allowedOnSouthEdge = {{allowedOnSouthEdge}};
        this.allowedOnEastEdge = {{allowedOnEastEdge}};

        this.relations_top = new Asset[] {
            {{relations_top}}
		};

		this.relations_down = new Asset[] {
			{{relations_down}}
		};

		this.relations_north = new Asset[] {
			{{relations_north}}
		};

		this.relations_west = new Asset[] {
			{{relations_west}}
		};

		this.relations_south = new Asset[] {
			{{relations_south}}
		};

		this.relations_east = new Asset[] {
			{{relations_east}}
		};
	}


    @Override
    public BlockState[][][] getStructure() {
        BlockState[][][] data = new BlockState[HEIGHT][WIDTH][WIDTH];

        {{structure}}

        return data;
    }

}
