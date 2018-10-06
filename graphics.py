# Graphics / Plotting

def plot(df):
    fig, ax = plt.subplots(nrows = 1, ncols = 1)
    ax.plot(df.transpose().values, alpha = 0.1)
    ax.plot(df.values.mean(axis=0), alpha = 1, linewidth=2, c="r")
    plt.show()


if __name__ == "__main__":
    from ir_model import *
    (bondPrices, YTM) = genModel(0.01,0.5)
    plot(YTM)

