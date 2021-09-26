package ua.iladrien.buildinggenerator.generator;

{{imports}}

import java.util.ArrayList;
import java.util.List;

public class Assets {

    protected static final List<Asset> registered = new ArrayList<>();

    {{assets}}

    private static Asset register(Asset asset) {
		registered.add(asset);
		return  asset;
	}

    public static ArrayList<Asset> getRegistered() {
		return new ArrayList<>(registered);
	}

	public static void registerAllRelations() {
    	for (Asset asset: registered)
    		asset.registerRelations();
	}

}
